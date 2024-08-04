from django.core.serializers.json import DjangoJSONEncoder
import json

class ModelToDictSerializer:
    @staticmethod
    def serialize(instance):
        """
        Serialize a Django model instance to a dictionary.
        """
        opts = instance._meta
        data = {}
        for field in opts.concrete_fields + opts.many_to_many:
            if field.is_relation and field.many_to_many:
                data[field.name] = list(field.value_from_object(instance).values_list('pk', flat=True))
            elif field.is_relation:
                value = field.value_from_object(instance)
                data[field.name] = value.pk if value else None
            else:
                data[field.name] = field.value_from_object(instance)
        return json.loads(json.dumps(data, cls=DjangoJSONEncoder))

    @staticmethod
    def serialize_many(instances):
        """
        Serialize a list of Django model instances to a list of dictionaries.
        """
        return [ModelToDictSerializer.serialize(instance) for instance in instances]

    @staticmethod
    def deserialize(model_class, data):
        """
        Deserialize a dictionary to a Django model instance.
        """
        instance = model_class()
        opts = model_class._meta
        for field in opts.concrete_fields + opts.many_to_many:
            if field.is_relation and field.many_to_many:
                # Handle many-to-many fields
                field_value = data.get(field.name, [])
                if field_value:
                    instance.save()  # Save instance before adding m2m relationships
                    getattr(instance, field.name).set(field_value)
            elif field.is_relation:
                # Handle foreign key fields
                field_value = data.get(field.name, None)
                if field_value:
                    related_instance = field.remote_field.model.objects.get(pk=field_value)
                    setattr(instance, field.name, related_instance)
            else:
                setattr(instance, field.name, data.get(field.name))
        return instance

    @staticmethod
    def deserialize_many(model_class, data_list):
        """
        Deserialize a list of dictionaries to a list of Django model instances.
        """
        return [ModelToDictSerializer.deserialize(model_class, data) for data in data_list]
