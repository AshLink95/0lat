# Overview
0lat is simple project that uses ZeroMQ, a very fast messaging parsing library. 0lat sets up a server, written in C, that has 2 sockets: a `REQ` socket for simple RPC and a `PUB` socket to output info to async loggers listening.

This is just a toy project. A networking sandbox, much closer to being a template for an inefficiently sophisticated system more than anything practical.

# Structure
The project is built with SCons. It produces 2 binary files:
* Server: written in C with 2 sockets.
* async logger: written in Rust with a `SUB` socket.

# Test
This repo contains a test file written in python. It builds the binaries and runs them then exchanges a few messages with the server in an *interesting* scenario.

The last line in the file is a commented scons cleaner subprocess initiator. Uncomment it if you want to clean the directory after the test run.

## Current Issues
* The first ever test will be slow because we will build a lot of cargo files.
* The first log run after the creation of the log file will display a single line. This is probably something that has to do with `tokio` or ZeroMQ but I'm yet to find a fix.
* I didn't configure SCons to detect changes in a rust cargo. So, make sure to remove the logger output file after editing the rust logger cargo.
