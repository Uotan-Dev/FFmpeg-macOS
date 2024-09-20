from argparse import ArgumentParser
from multiprocessing import cpu_count
import pathlib
import sys
import os


def execute(command: str):
    print(f"Execute: {command}.")
    os.system(command)


if __name__ == "__main__":
    parser = ArgumentParser(description="Configure & Make & Install FFmpeg.")
    parser.add_argument("--ffmpeg_dir", type=str, default=os.getcwd(), help='indicate FFmpeg dir.')
    parser.add_argument("--target_dir", type=str, default=os.getcwd(), help='indicate target dir.')
    args = parser.parse_args()
    ffmpeg_dir = pathlib.Path(args.ffmpeg_dir).absolute()
    target_dir = pathlib.Path(args.target_dir).absolute()
    print(f"Compile... {ffmpeg_dir}")


    def make(arch: str):
        n_cpu = cpu_count()
        print("Configure project.")
        execute(
            f"cd {ffmpeg_dir} && ./configure --enable-cross-compile --prefix={target_dir / ('install_' + arch + '/')} "
            f"--enable-static --disable-runtime-cpudetect --disable-doc --enable-swresample --disable-swscale --disable-postproc --disable-avfilter --disable-debug --enable-audiotoolbox --disable-sdl2 --enable-videotoolbox --enable-opencl --enable-gpl --disable-shared --disable-iconv --arch={arch} --cc='clang -w -arch {arch}'"
        )
        print(f"Make project ({n_cpu} threads).")
        execute(f"cd {ffmpeg_dir} && make -j{n_cpu}")
        print(f"Install project.")
        execute(f"cd {ffmpeg_dir} && make install")


    print("----------arm64----------")
    clean()
    make("arm64")
    print("----------x86_64----------")
    clean()
    make("x86_64")
