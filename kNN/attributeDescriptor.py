from enum import Enum

class AttributeType(Enum):
    NOMINAL = 1
    CONTINUOUS = 2
    LABEL = 3

class AttributeDescriptor:

    def __init__(self, attribute_type, attribute_values=None):
        self.attribute_type = attribute_type
        self.attribute_values = attribute_values

    def get_attribute_type(self):
        return self.attribute_type

    def get_attribute_values(self):
        return self.attribute_values


def get_attribute_descriptors():
    attributes = []

    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['b', 'a'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['u','y','l','t'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['g','p','gg'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['c', 'd', 'cc', 'i', 'j', 'k', 'm', 'r', 'q', 'w', 'x', 'e', 'aa', 'ff'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['v', 'h', 'bb', 'j', 'n', 'z', 'dd', 'ff', 'o'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['t','f'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['t','f'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['t','f'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.NOMINAL, ['g','p','s'])
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.CONTINUOUS)
    attributes.append(attribute)
    attribute = AttributeDescriptor(AttributeType.LABEL, ['+','-'])
    attributes.append(attribute)

    return attributes
