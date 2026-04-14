# Word Saver — Build Caveats

## macOS Accessibility Permissions

pynput requires **Accessibility** (and on macOS 10.15+, **Input Monitoring**) permissions.

macOS ties these permissions to the app's **code signature**. Every `py2app` rebuild produces a new ad-hoc signature, which **invalidates** the existing permission entry.

### After every rebuild

1. Open **System Settings → Privacy & Security → Accessibility**
2. **Remove** the old `word-saver` entry (minus button)
3. **Add** the newly built `/Applications/word-saver.app` (plus button)
4. Repeat for **Input Monitoring** if the hotkey still doesn't work

Toggling off/on is **not enough** — you must remove and re-add.

### How to verify trust

```bash
# This will always say "not trusted" — terminal has its own identity:
/Applications/word-saver.app/Contents/MacOS/word-saver

# This is the correct way — launches with the app's identity:
open -a word-saver
```

Running the binary directly from the terminal uses the **terminal's** code identity, not the app's. Always test with `open -a`.

## Reopening the App

The `reopen_word_saver.zsh` script sends `SIGTERM` and waits for the process to die before launching a new instance. Without the wait, `open -a` sees the old (dying) process and silently refuses to start a new one.

## Known pynput Issue: Event Tap Timeout

macOS can disable a `CGEventTap` via `kCGEventTapDisabledByTimeout` if the callback is slow. pynput (as of 1.8.x) does **not** handle this — the hotkey silently stops working after ~30 minutes.

Workaround: use the reopen script periodically, or patch `pynput/_util/darwin.py` in the venv before building:

```python
# In the Quartz imports, add:
kCGEventTapDisabledByTimeout,
kCGEventTapDisabledByUserInput,

# In _run(), after tap = self._create_event_tap():
self._tap = tap

# In _handler(), before the existing body:
if event_type in (kCGEventTapDisabledByTimeout, kCGEventTapDisabledByUserInput):
    if self._tap is not None:
        CGEventTapEnable(self._tap, True)
    return None
```
