# pyright: reportUndefinedVariable=false
from os import environ
out1 = ARGUMENTS.get("out1")
out2 = ARGUMENTS.get("out2")
SetOption('experimental', 'ninja')

# Create builders
def build_cargo(target, source, env):
    ret = 0
    for t, s in zip(target, source):
        cmd = f"cd {s} && cargo build --quiet && mv target/debug/{s} ../{t} && cd .."
        print(f"Running: {cmd}")
        ret = env.Execute(cmd)
        if (ret != 0):
            break;
    return ret

# Create Cleaners
def clean_cargo(target, source, env):
    ret = 0
    if not isinstance(target, (list, tuple)):
        target = [target]
    if not isinstance(source, (list, tuple)):
        source = [source]
    for t, s in zip(target, source):
        print(target, source)
        cmd = f"rm {t} && cd {s} && cargo clean --quiet"
        print(f"Removed {t}")
        print(f"Cleaned {s}")
        ret = env.Execute(cmd)
        if ret != 0:
            return ret
    return 0

# Register builders
rust_builder = Builder(action=build_rust, suffix='', src_suffix='.rs')
cargo_builder = Builder(action=build_cargo, source_factory=Dir)

# Environment
env = Environment(BUILDERS={'Rust': rust_builder, 'Cargo': cargo_builder}, ENV={'PATH': environ['PATH']}, LIBS=['zmq'])

# Build
env.Program(out1, 'server.c')
env.Cargo(out2, 'rust_logger')

# Clean
if env.GetOption('clean'):
    clean_cargo(out2, 'rust_client', env)
