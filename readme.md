<center><h1> HLS Downloader </h1></center>

<center>An efficient, fast, powerful and light-weight HLS downloader that doesn't require `ffmpeg`. </center>

### Core features:

- Auto-quality fallback if quality is unavailable.
- Implements internal AES decryption.
- Supports an optional progress bar `tqdm`.
- Checks HLS streams recursively to extract all qualities forehand.
- Supports custom headers and unverified SSL urls.

Project made in favor of [AnimDL](https://github.com/justfoolingaround).

### Limitations

- Cannot download m3u8 pulls (IPTV and things like that)

### Disclaimer

Downloads are done in `ts` extension. To get seamless and error-free playback, using mpv is recommended.