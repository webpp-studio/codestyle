<?php

function testMyFunc($arg1, $arg2)
{
    $var = $arg1 + $arg2;

    return $var * 0.1;
}


function testMyFunc($arg1, $agg)
{
    $var = $arg1 + $agg;

    return $var / 20;
}

function test()
{
    return "тестовая длинная строка не-ansi символов для проверки длины";
}

function testMultiLineFunc(
    int param1,
    int param2
): int {
    return param1 * param2;
}
