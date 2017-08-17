import keras.backend
import tensorflow


def shuffle(x):
    """
    Modify a sequence by shuffling its contents. This function only shuffles
    the array along the first axis of a multi-dimensional array. The order of
    sub-arrays is changed but their contents remains the same.
    """
    return tensorflow.random_shuffle(x)


def gather_nd(params, indices):
    return tensorflow.gather_nd(params, indices)


def matmul(a, b, transpose_a=False, transpose_b=False, adjoint_a=False, adjoint_b=False, a_is_sparse=False, b_is_sparse=False):
    return tensorflow.matmul(a, b, transpose_a=transpose_a, transpose_b=transpose_b, adjoint_a=adjoint_a, adjoint_b=adjoint_b, a_is_sparse=a_is_sparse, b_is_sparse=b_is_sparse)


# TODO: emulate NumPy semantics
def argsort(a):
    _, indices = tensorflow.nn.top_k(a, keras.backend.shape(a)[-1])

    return indices


def scatter_add_tensor(ref, indices, updates, name=None):
    """
    Adds sparse updates to a variable reference.

    This operation outputs ref after the update is done. This makes it easier to chain operations that need to use the
    reset value.

    Duplicate indices: if multiple indices reference the same location, their contributions add.

    Requires updates.shape = indices.shape + ref.shape[1:].
    :param ref: A Tensor. Must be one of the following types: float32, float64, int64, int32, uint8, uint16,
        int16, int8, complex64, complex128, qint8, quint8, qint32, half.
    :param indices: A Tensor. Must be one of the following types: int32, int64. A tensor of indices into the first
        dimension of ref.
    :param updates: A Tensor. Must have the same dtype as ref. A tensor of updated values to add to ref
    :param name: A name for the operation (optional).
    :return: Same as ref. Returned as a convenience for operations that want to use the updated values after the update
        is done.
    """
    with tensorflow.name_scope(name, 'scatter_add_tensor', [ref, indices, updates]) as scope:
        ref = tensorflow.convert_to_tensor(ref, name='ref')

        indices = tensorflow.convert_to_tensor(indices, name='indices')

        updates = tensorflow.convert_to_tensor(updates, name='updates')

        ref_shape = tensorflow.shape(ref, out_type=indices.dtype, name='ref_shape')

        scattered_updates = tensorflow.scatter_nd(indices, updates, ref_shape, name='scattered_updates')

        with tensorflow.control_dependencies([tensorflow.assert_equal(ref_shape, tensorflow.shape(scattered_updates, out_type=indices.dtype))]):
            output = tensorflow.add(ref, scattered_updates, name=scope)

        return output


def meshgrid(*args, **kwargs):
    return tensorflow.meshgrid(*args, **kwargs)


newaxis = tensorflow.newaxis


def where(condition, x=None, y=None):
    return tensorflow.where(condition, x, y)


def non_maximum_suppression(boxes, scores, maximum, threshold=0.5):
    return tensorflow.image.non_max_suppression(boxes=boxes, iou_threshold=threshold, max_output_size=maximum, scores=scores)


def crop_and_resize(image, boxes, size):
    """Crop the image given boxes and resize with bilinear interplotation.
    # Parameters
    image: Input image of shape (1, image_height, image_width, depth)
    boxes: Regions of interest of shape (1, num_boxes, 4),
    each row [y1, x1, y2, x2]
    size: Fixed size [h, w], e.g. [7, 7], for the output slices.
    # Returns
    4D Tensor (number of regions, slice_height, slice_width, channels)
    """
    box_ind = keras.backend.zeros_like(boxes, "int32")
    box_ind = box_ind[..., 0]
    box_ind = keras.backend.reshape(box_ind, [-1])

    boxes = keras.backend.reshape(boxes, [-1, 4])

    return tensorflow.image.crop_and_resize(image, boxes, box_ind, size)


def squeeze(a, axis=None):
    """
    Remove single-dimensional entries from the shape of an array.
    """
    return tensorflow.squeeze(a, axis)
