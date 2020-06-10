<?php

namespace foo;

/**
 * Class Vendor\Foo
 * @tag tag
 */
class FooTest
{

}

/**
 * Foo docks
 * @param int $arg1 arg1 comment
 * @param int $arg2 arg2 comment
 * @return float
 */
function testFunc(int $arg1, int $arg2)
{
    require 'foo.php';

    $var = $arg1 + $arg2;

    return $var * 0.1;
}

/**
 * Foo docks
 *
 * @param int $arg1 comment
 * @param int $agg comment
 * @return float
 */
function testMyFunc(int $arg1, int $agg): float
{
    $var = $arg1 + $agg;

    return (float) $var / 20;
}

/**
 * Foo docks
 *
 * @return string
 */
function test()
{
    return "тестовая длинная строка не-ansi символов для проверки длины";
}

/**
 * @param int $param1 comment
 * @param int $param2 comment
 * @return int
 */
function testMultiLineFunc(
    int $param1,
    int $param2
): int {
    return $param1 * $param2;
}
