# Fly_in

## subject

- 📙 [Fly_in subject](subject/Fly_in.pdf)

<div align="center">

⭐ Have fun learning and coding ⭐

</div>

<br>

---

<br><br><br> 

## what i should start with ?

```.py
run: make or make help 
```

<br><br><br> 

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

-> OSError happens when the OS says:
“I cannot do what your program requested.”


---

## models

### From the subject, what are the main things?

- A zone (hub, start_hub, end_hub)
- A connection between zones
- A graph that contains everything

### Next question:

#### Should a Zone know about connections?

My recommendation:

No.

Keep it simple first.

A zone should only describe itself.

The graph will know how zones are connected.


### the plan i manage to go with it in parsing

#### Phase 1 — Load

- load raw data
- clean it
- index it

#### Phase 2 — Extract
- extract nb_drones
- extract all hubs
- extract all connections

#### Phase 3 — Validate
- validate nb_drones
- validate hubs
- validate connections
- validate relationships between them

#### Phase 4 — Build
- build graph
- return it

#### Dispatcher is just the orchestrator — it calls the phases in order, nothing more:

dispatcher()
    → data = load()
    → extracted = extract(data)
    → validate(extracted)
    → graph = build(extracted)
    → return graph

