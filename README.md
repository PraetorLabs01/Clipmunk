# Clipmunk

Pull your gaming clips from any capture app, trim them, shrink them to fit Discord, and drag them straight into chat, or post them to your server's channel in one click.

Free and open source, for Windows 10 and 11. Website: [praetorlabshq.com/clipmunk](https://praetorlabshq.com/clipmunk/)

## Download

**[Download Clipmunk-Setup.exe](https://github.com/PraetorLabs01/Clipmunk/releases/latest/download/Clipmunk-Setup.exe)**, run it, done: desktop icon, Start menu entry, uninstall from Windows settings. No admin needed.

Windows may say "Windows protected your PC" because the installer isn't code-signed yet: click **More info → Run anyway**. Each release lists the installer's SHA-256 checksum if you want to check your download.

Works on any Windows PC: it compresses with your NVIDIA / AMD / Intel GPU if you have one, otherwise the CPU. When there's a new version, Clipmunk offers it with a popup; nothing downloads until you press **Update now**.

## Using it

1. **Find my clip folders** finds where OBS, ShadowPlay / NVIDIA App, AMD ReLive, Medal, Xbox Game Bar and Outplayed save. Or **+ Add folder** for any folder. Add as many as you like; sub-folders are included.
2. New clips appear on their own (marked **NEW**) once they finish saving.
3. Pick a clip and drag the green handles to trim (or **I** / **O** at the playhead). Space plays, ← → skip 1 s (Shift = 5 s), `,` `.` step one frame, scroll on the timeline to zoom.
4. Choose **Fit under**: Discord free 20 MB, Nitro Basic 50 MB, Nitro 500 MB, or a custom size. It's remembered. Clipmunk picks the resolution and frame rate that look best at that size, and warns you when a clip is too long to stay sharp.
5. **Compress for Discord** (Ctrl+Enter). Then drag the **Drag me into Discord** card into a chat, or just press Ctrl+V in Discord (it's copied automatically).

You can also drag any clip straight from the list; it sends the compressed copy if there is one.

**Compressed clips** (sidebar) shows how much space the smaller copies take, and lets you open the folder, delete some, or empty it. Copies older than 30 days go to the Recycle Bin on their own (change or turn this off there). Only files Clipmunk made are ever touched; your recordings are left alone.

## Sharing to your Discord server

**Share to Discord** posts a finished clip into a channel through a Discord webhook (no bot needed). Settings → Discord sharing → **How to set up sharing** walks through it.

- **Server admins:** in Discord, Edit Channel → Integrations → Webhooks → New Webhook → Copy Webhook URL. In Clipmunk, **Add channel** and paste it. Then select it and press **Copy invite**, and post that in your server.
- **Everyone else:** copy the invite from Discord and open Clipmunk. It asks to add the channel. (Or Settings → **Paste invite**.)

Posts use your server's upload limit (20 MB, or 50 / 100 MB on boosted servers), not Nitro. If a clip is bigger, Share makes a copy that fits and sends that.

Anyone with a webhook link or invite can post to that channel, so only share them inside your own server. If one leaks, delete the webhook in Discord and post a new invite.

## Privacy

Clipmunk has no accounts, no analytics and no crash reports. It only goes online to:

- check GitHub for a new version (a few seconds after it opens, then every 6 hours), and download it if you press Update;
- check a Discord webhook once when you add a channel;
- post a clip, your optional message and "*your name* via Clipmunk" when you press Share.

It reads the clipboard on your PC only to spot Clipmunk invites, and asks before adding anything. Settings (including your channels' webhook links) are stored in `%APPDATA%\ClipDrop`, with a thumbnail cache in `%LOCALAPPDATA%\ClipDrop` ("ClipDrop" was Clipmunk's old name). Uninstalling leaves these folders; delete them to remove everything.

## Problems or ideas

Open an [issue](https://github.com/PraetorLabs01/Clipmunk/issues). Please include your Clipmunk version (Settings → About & licenses), your graphics card and the capture app you use. For anything private, such as a security problem, email praetorlabs@gmail.com instead (see [SECURITY.md](SECURITY.md)).

## Developing

- `run.bat` runs from source (sets up `.venv` and downloads FFmpeg the first time).
- `build.bat` makes `Clipmunk-Setup.exe` (needs Inno Setup: `winget install JRSoftware.InnoSetup --scope user`). Builds never contain anyone's Discord channels.
- `release.bat "what changed"` bumps the version, builds, tags the pushed commit and publishes a GitHub release; everyone's Clipmunk offers the update next time it opens.

Code: `clipdrop/compress.py` (size targeting), `library.py` (folder watching), `finder.py` (capture-app folders), `share.py` and `invite.py` (Discord), `ui/` (Qt windows).

## License

Clipmunk is free software under the [GNU GPL v3](LICENSE), with no warranty. It ships FFmpeg, Qt / PySide6, Python and other open-source parts, each under its own license: see [THIRD-PARTY-NOTICES.txt](THIRD-PARTY-NOTICES.txt).

Made by [Praetor Labs](https://praetorlabshq.com/).
