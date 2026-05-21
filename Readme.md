# Fly_in

## subject

- 📙 [Fly_in subject](subject/Fly_in.pdf)

<div align="center">

⭐ Have fun learning and coding ⭐

</div>

---

## OSError?

- OSError is an exception raised when the operating system fails to perform a system-level operation requested by your program.

### What is a “system-level operation”?

Things like:

- opening a file
- creating/deleting folders
- accessing permissions
- reading from disk
- network/socket operations
- interacting with processes/devices

### Why does it happen?

Because Python itself does not control the hardware directly.
It asks the operating system (Linux, Windows, macOS) to do the work.

If the OS cannot do it, Python raises OSError or one of its subclasses.

> A system-level operation is any operation where your program must ask the operating system to access or manage real computer resources such as files, hardware, memory, processes, or networking.

```

-> OSError happens when the OS says:
“I cannot do what your program requested.”


BaseException
└── Exception
    └── OSError
        ├── FileNotFoundError
        ├── PermissionError
        ├── IsADirectoryError
        ├── TimeoutError
        ├── ConnectionError
        └── ...
```

---

