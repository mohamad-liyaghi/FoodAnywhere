from rest_framework import mixins
from rest_framework.generics import GenericAPIView


class UpdateDestroyAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    """
    Concrete view for updating or deleting a model instance.
    """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
