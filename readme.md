<img src="https://capsule-render.vercel.app/api?type=soft&fontColor=F2003C&text=hlsdl.py&height=150&fontSize=60&desc=A%20HTTP%20Live%20Stream%20Downloader&descAlignY=75&descAlign=60&color=00000000&animation=twinkling">

> **Note**: Use this project only when ffmpeg is unavailable. 
> 
>```console
> $ ffmpeg -i $HLS_URL -c copy $OUTFILE.TS -hide_banner
> [hls @ ...] ...
> ```
> This is because ffmpeg has a massively better arsenal and may be more reliable. for normal cases, this project will suffice.

This project is created for references and as a port to a much powerful counterpart in Rust. In most cases, this project may be performant than ffmpeg. 

## Livestream Downloading

This project provides code for live stream downloading but does not implement that in the CLI.

## Usage

```console
$ py hlsdl.py --help                                                                                                                                                                Usage: hlsdl.py [OPTIONS] URL                                                                                                                                                                                                                                                                                                                                                 Options:                                                                                                                                                                                 -f, --file PATH                 File to output to.
  --strict                        Strictly follow the HLS specification. This
                                  will cause the program to fail if it
                                  encounters a non-compliant stream.
  -nv, --no-verify                Don't verify the SSL certificate.
  -t, --timeout INTEGER           The timeout for the request.
  -d, --data STRING-OR-PIPE       The data to send with the request; changes
                                  method to POST if method isn't POST or
                                  PATCH.
  -m, --method [GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|TRACE]
                                  The method to use for the request.
  --headers KEY-VALUE-PAIR        The headers to add to the request.
  -p, --params KEY-VALUE-PAIR     The parameters to add with the URL.
  --help                          Show this message and exit.
```