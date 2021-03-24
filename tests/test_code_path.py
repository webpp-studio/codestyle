"""Проверки модуля code_path."""
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, call, patch

from codestyle import code_path
from codestyle.code_path import ExpandedPathTree


class TestExpandedPathTree(TestCase):
    """Проверка ExpandedPathTree."""

    @patch.object(
        ExpandedPathTree,
        '_ExpandedPathTree__generate_paths',
        new_callable=Mock,
    )
    @patch.object(
        ExpandedPathTree,
        'check_path_availability',
        new=Mock(),
    )
    def test_path_gen(self, mocked_path_gen_getter: Mock):
        """Проверка path_gen."""
        mock_getter_iter = Mock(return_value=iter([]))
        mocked_path_gen_getter.return_value = Mock(
            __iter__=mock_getter_iter
        )

        tree = ExpandedPathTree(Path('test.py'))
        mock_target = Mock()
        mock_iter = Mock(return_value=iter([mock_target]))
        tree.targets = Mock(__iter__=mock_iter)
        list(tree.path_gen())

        self.assertEqual(True, mock_iter.called)
        self.assertEqual(1, mock_iter.call_count)
        args, kwargs = mock_iter.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_path_gen_getter.called)
        self.assertEqual(1, mocked_path_gen_getter.call_count)
        args, kwargs = mocked_path_gen_getter.call_args
        self.assertTupleEqual((mock_target,), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(
        ExpandedPathTree,
        'check_path_availability',
        new_callable=Mock,
    )
    def test_init(self, mocked_path_checker: Mock):
        """Проверка инициализации."""
        mock_targets = [Mock(), Mock()]

        ExpandedPathTree(*mock_targets)

        self.assertEqual(True, mocked_path_checker.called)
        self.assertEqual(1, mocked_path_checker.call_count)
        args, kwargs = mocked_path_checker.call_args
        self.assertTupleEqual((tuple(mock_targets),), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(
        ExpandedPathTree,
        'check_path_availability',
        new=Mock,
    )
    def test_is_excluded_returns_false(self):
        """Проверка возвращения False для __is_excluded метода."""
        mock_exclude = Mock()
        mock_match = Mock(return_value=False)

        tree = ExpandedPathTree(Mock(), excludes=(mock_exclude,))
        result = tree._ExpandedPathTree__is_excluded(Mock(match=mock_match))

        self.assertEqual(False, result)

        self.assertEqual(True, mock_match.called)
        self.assertEqual(1, mock_match.call_count)
        args, kwargs = mock_match.call_args
        self.assertTupleEqual((mock_exclude,), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(
        ExpandedPathTree,
        'check_path_availability',
        new=Mock,
    )
    def test_is_excluded_returns_true(self):
        """Проверка возвращения True для __is_excluded метода."""
        tree = ExpandedPathTree(Mock(), excludes=(Mock(),))
        result = tree._ExpandedPathTree__is_excluded(
            Mock(match=Mock(return_value=True))
        )

        self.assertEqual(True, result)

    def test_check_path_availability_with_missing_paths(self):
        """Проверка метода с набором отсутствующих путей."""
        mock_exists = Mock(return_value=False)
        mock_str = Mock(return_value='/mock-path/')
        mock_paths = [Mock(exists=mock_exists, __str__=mock_str)]

        with self.assertLogs(
            logger=code_path.__name__, level='INFO'
        ) as context_manager:
            ExpandedPathTree.check_path_availability(mock_paths)

        self.assertIn(
            'INFO:codestyle.code_path:Проверяю какие тут пути ты мне '
            'указал...',
            context_manager.output,
        )

    @patch.object(
        ExpandedPathTree, '_ExpandedPathTree__is_excluded', new_callable=Mock
    )
    @patch.object(ExpandedPathTree, 'check_path_availability', new=Mock)
    def test_generate_paths_for_excluded_path(self, mocked_is_excluded: Mock):
        """Проверка __generate_paths для исключённого пути."""
        mock_path = Mock()
        mocked_is_excluded.return_value = True

        tree = ExpandedPathTree(Mock(), excludes=(Mock(),))
        result = tree._ExpandedPathTree__generate_paths(mock_path)

        self.assertEqual([], list(result))

        self.assertEqual(True, mocked_is_excluded.called)
        self.assertEqual(1, mocked_is_excluded.call_count)
        args, kwargs = mocked_is_excluded.call_args
        self.assertTupleEqual((mock_path,), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(
        ExpandedPathTree,
        '_ExpandedPathTree__is_excluded',
        new=Mock(return_value=False),
    )
    @patch.object(ExpandedPathTree, 'check_path_availability', new=Mock)
    def test_generate_paths_yields_file_path(self):
        """Проверка, что генератор возвращает только пути к файлам."""
        mock_is_file = Mock(return_value=True)
        mock_file_path = Mock(is_file=mock_is_file)

        tree = ExpandedPathTree(Mock(), excludes=(Mock(),))
        result = tree._ExpandedPathTree__generate_paths(mock_file_path)

        self.assertEqual([mock_file_path], list(result))

        self.assertEqual(True, mock_is_file.called)
        self.assertEqual(1, mock_is_file.call_count)
        args, kwargs = mock_is_file.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

    @patch.object(
        ExpandedPathTree, '_ExpandedPathTree__is_excluded', new_callable=Mock
    )
    @patch.object(ExpandedPathTree, 'check_path_availability', new=Mock)
    def test_generate_path(self, mocked_is_excluded: Mock):
        """Проверки __generate_paths метода."""
        mock_is_file = Mock(return_value=True)
        mock_file_path = Mock(is_file=mock_is_file)
        mock_iterdir = Mock(return_value=iter([mock_file_path]))

        mocked_is_excluded.return_value = False

        tree = ExpandedPathTree(Mock(), excludes=(Mock(),))
        result = tree._ExpandedPathTree__generate_paths(
            Mock(is_file=Mock(return_value=False), iterdir=mock_iterdir)
        )

        self.assertEqual([mock_file_path], list(result))

        self.assertEqual(True, mock_iterdir.called)
        self.assertEqual(1, mock_iterdir.call_count)
        args, kwargs = mock_iterdir.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)

        self.assertEqual(True, mocked_is_excluded.called)
        self.assertEqual(2, mocked_is_excluded.call_count)
        self.assertIn(call(mock_file_path), mocked_is_excluded.mock_calls)

        self.assertEqual(True, mock_is_file.called)
        self.assertEqual(1, mock_is_file.call_count)
        args, kwargs = mock_is_file.call_args
        self.assertTupleEqual((), args)
        self.assertDictEqual({}, kwargs)
