# console.py
A pythonic 2.7 implementation, without dependencies, of 'please drop this to console' for *nix systems.

## Reasoning
I've written this enough times that it's starting to get complicated, and reliable. That's as good a time as any to pull it out of my personal projects and throw it on github with a clear license so I can start copying this into my professional projects.

It asynchronously populates queues for Stdin and Stderr, making it reliably handle large blocks of text or long running processes. When scripting multiple programs, console allows the high level script flow and logic to be in python (as logic should be!) while maintaining the flexibility of shell scripts for launching programs and parsing output.
