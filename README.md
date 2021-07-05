# truetime
Estimate "real" time in _very_ adverse conditions:
- offline
- system clock cannot be trusted (eg. user keeps changing the time forwards and/or backwards in time).
  - user may also shut down/put to sleep/hibernate system for abnormal periods of time.
- this script is _NOT_ running in the background, and only allowed to run occasionally.

**Warning: this is experimental, use at your own risk.**


### Assumptions
- Assumes system interacts w/ temp directory files on a roughly continuous and consistent basis.

### How it works

Uses an NTP server when online.

When offline, estimates time from system temp directory files.



Steps:
1. get earliest timestamp that appears trustable
    - scan all files in temp dir, storing timestamps for file creation, file modification, and file last accessed
    - calculate gaps between those timestamps
    - earliest trustable timestamp is the time before earliest gap
2. calculate how much time has elapsed since that time
    - TBD
3. add the offset to the earlier timestamp
