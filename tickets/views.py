from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket
from .serializers import TicketSerializer
from django.core.cache import cache

# Cache key used for the ticket list
TICKET_LIST_CACHE_KEY = "ticket_list"


class TicketViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ticket CRUD.
    - GET /tickets/    → returned from Redis cache (5 min TTL)
    - POST/PATCH/DELETE → invalidates the cache so the next GET is fresh
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['category', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'created_at']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        """Override list to serve from Redis cache when possible."""
        # Build a unique cache key that includes query params (filters, search, page…)
        query_string = request.META.get('QUERY_STRING', '')
        cache_key = f"{TICKET_LIST_CACHE_KEY}:{query_string}"

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            # Cache HIT — return cached response directly
            from rest_framework.response import Response
            return Response(cached_data)

        # Cache MISS — fetch from DB as normal
        response = super().list(request, *args, **kwargs)

        # Store result in Redis (inherits TIMEOUT from settings; default 300 s)
        cache.set(cache_key, response.data)
        return response

    def _invalidate_cache(self):
        """Delete all ticket list cache entries from Redis."""
        # django-redis supports pattern-based deletion; clear all ticket_list:* keys
        try:
            cache.delete_pattern(f"{TICKET_LIST_CACHE_KEY}:*")
        except AttributeError:
            # Fallback for non-Redis backends (e.g., LocMemCache in tests)
            cache.clear()

    def perform_create(self, serializer):
        """Invalidate cache after a new ticket is created."""
        super().perform_create(serializer)
        self._invalidate_cache()

    def perform_update(self, serializer):
        """Invalidate cache after a ticket is updated."""
        super().perform_update(serializer)
        self._invalidate_cache()

    def perform_destroy(self, instance):
        """Invalidate cache after a ticket is deleted."""
        super().perform_destroy(instance)
        self._invalidate_cache()
