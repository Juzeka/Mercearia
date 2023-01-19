class ProdutoServices:
    def __init__(self, *args, **kwargs):
        self.data = kwargs.get('data')
        self.serializer = kwargs.get('serializer')

    def serialize_and_save(self):
        serializer = self.serializer(data=self.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return serializer
