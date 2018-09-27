import unittest

import numpy as np
import tensorflow as tf
import tensorflow_encrypted as tfe


class TestReduceSum(unittest.TestCase):
    def setUp(self):
        tf.reset_default_graph()

    def test_reduce_sum_1d(self):
        config = tfe.LocalConfig([
            'server0',
            'server1',
            'crypto_producer'
        ])

        t = [1, 2]
        with tf.Session() as sess:
            out = tf.reduce_sum(t)
            actual = sess.run(out)

        with tfe.protocol.Pond(*config.get_players('server0, server1, crypto_producer')) as prot:
            b = prot.define_private_variable(tf.constant(t))
            out = prot.reduce_sum(b)

            with config.session() as sess:
                sess.run(tf.global_variables_initializer())
                final = out.reveal().eval(sess)

        np.testing.assert_array_equal(final, actual)

    def test_reduce_sum_2d(self):
        config = tfe.LocalConfig([
            'server0',
            'server1',
            'crypto_producer'
        ])

        t = [[1, 2], [1, 3]]
        with tf.Session() as sess:
            out = tf.reduce_sum(t, axis=1)
            actual = sess.run(out)

        with tfe.protocol.Pond(*config.get_players('server0, server1, crypto_producer')) as prot:
            b = prot.define_private_variable(tf.constant(t))
            out = prot.reduce_sum(b, axis=1)

            with config.session() as sess:
                sess.run(tf.global_variables_initializer())
                final = out.reveal().eval(sess)

        np.testing.assert_array_equal(final, actual)

    def test_reduce_sum_huge_vector(self):
        config = tfe.LocalConfig([
            'server0',
            'server1',
            'crypto_producer'
        ])

        t = [1] * 2**13
        with tf.Session() as sess:
            out = tf.reduce_sum(t)
            actual = sess.run(out)

        with tfe.protocol.Pond(*config.get_players('server0, server1, crypto_producer')) as prot:
            b = prot.define_private_variable(tf.constant(t))
            out = prot.reduce_sum(b)

            with config.session() as sess:
                sess.run(tf.global_variables_initializer())
                final = out.reveal().eval(sess)

        np.testing.assert_array_equal(final, actual)


if __name__ == '__main__':
    unittest.main()
