"""A Docstring can be added the head of any module.

Any element in the module can also have a docstring.
If there is only one docstring before the first element,
it is assumed to be a module docstring.
"""

"""A docstring for add function"""
can add(a: int, b: int) -> int {
    return a + b;
}
# No docstring for subtract function

can subtract(a: int, b: int) -> int {
    return a - b;
}

with entry:__main__ {
    print(add(1, subtract(3, 1)));
}

glob x: int = 10;

enum Colorenum {
    RED,
    GREEN,
    BLUE
}

obj Colour1 {
    has color1: Colorenum,
        point1: int;

    can get_color1 -> Colorenum;
}

:obj:Colour1:can:get_color1 -> Colorenum {
    return self.color1;
}

obj red :Colour1: {
    has base_colorred: Colorenum = Color.RED,
        pointred: int = 10;
    obj color2 {
        has color22: Color = Colorenum.BLUE,
            point22: int = 20;
    }
}

with entry:__main__ {
    r = red(color1=Color.GREEN, point1=20);
    print(r.get_color1());
    print(r.color2.color22);
}
