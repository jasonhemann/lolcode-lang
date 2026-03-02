# Flag-Wars-3-LOLCODE

Source code for the game Flag Wars 3: America Invaders made in LOLCODE.

Depends on:
- Raylib 4.x
- LOLCODE 1.4 with raylib bindings (see below)

This code as it is won't run on any LOLCODE interpreter because it is necessary to add raylib to it.

Watch on Youtube (click the image):

[![IMAGE ALT TEXT HERE](https://i3.ytimg.com/vi/jZorWrmubys/maxresdefault.jpg)](https://www.youtube.com/watch?v=jZorWrmubys)

# lci bindings

[Bindings here.](https://gist.github.com/SomeUnusualGames/4b9239eeacedde28182a244655cc1746)

This is my implementation of lci `bindings.c` adding some of raylib's functions. I used raylib 4.0, but since the functions used are pretty simple it should work on most future versions.

## Adding raylib functions to LOLCODE

The whole process is so simple it could be automated with a script, but first you have to do it by hand. In `bindings.c`:
```c
// For consistency, every function should be called *[yourCFunction]Wrapper
ReturnObject *YourCFunctionWrapper(struct scopeobject *scope)
{
    // First, get the parameters out of the scope:
    // (if your function doesn't take parameters, skip this step)
    ValueObject *arg0 = getArg(scope, "firstIntParameter");
    // You can use the macros defined in interpreter.h to get the actual values out of ValueObject
    int firstParam = getInteger(arg0);
    // Let's say your second parameter is raylib's Vector2 struct
    // Check below how to implement a custom struct
    ValueObject *arg1 = getArg(scope, "secondVector2Parameter");
    Vector2 vec = getVector2(arg1);

    // Call your function:
	int resultValue = YourCFunction(firstParam, vec);
    // To return a value to LOLCODE, you have to create the objects:
	ValueObject *ret = createIntegerValueObject(resultValue);
	return createReturnObject(RT_RETURN, ret);
    // If your function doesn't return anything, use:
    // return createReturnObject(RT_DEFAULT, NULL);
}
```
Finally, load the binding:
```c
loadBinding(lib, "YOURLOLCODEFUNCTION", "firstIntParameter secondVector2Parameter", &YourCFunctionWrapper);
```

`YOURLOLCODEFUNCTION` is how the function would be called from LOLCODE.

---
To implement a custom struct:

In interpreter.h:
- Add a `#define` macro to get the value: `#define getVector2(data) (value->data.vector2)`
- Add an extra value in ValueType enum: `VT_VECTOR2`
- Add a member in the ValueData union: `Vector2 vector2`

In interpreter.c:

The body of these functions pretty much do the same thing with the different variables.
```c
ValueObject *createVector2ValueObject(Vector2 vector2)
{
	ValueObject *p = malloc(sizeof(ValueObject));
	if (!p) {
		perror("malloc");
		return NULL;
	}
	p->type = VT_VECTOR2;
	p->data.vector2 = vector2;
	p->semaphore = 1;
	return p;	
}
```
And that's it.

## LOLCODE and Windows

If you're a loser like me and use Windows, you need to change a couple extra things to compile for this toy OS:

- Remove: `<readline/readline.h>`, `<readline/history.h>`, `inet.h` and the `SOCKS` bindings.
- Replace `getopt` with [`ya_getopt`](https://github.com/kubo/ya_getopt). Replace it also in `CMakeLists.txt`

Regardless of your OS you need to add raylib and its dependencies to CMake, for Windows it's: `target_link_libraries(lci m raylib winmm kernel32 gdi32)`
