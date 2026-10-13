/*
 * Compatibility for hosts exposing /proc/self/exe but not /proc/<pid>/exe.
 * Lean 4.34.1's lean_io_app_path uses the latter for its own process.
 * This interposer redirects ONLY that same-process executable-path lookup.
 * It does not change Lean's kernel or proof terms and grants no other access.
 * Ordinary hosts do not require it.
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buffer, size_t size) {
    static ssize_t (*real_readlink)(const char *, char *, size_t);
    if (!real_readlink)
        real_readlink = dlsym(RTLD_NEXT, "readlink");
    char own_path[64];
    snprintf(own_path, sizeof own_path, "/proc/%d/exe", (int)getpid());
    return real_readlink(strcmp(path, own_path) == 0 ? "/proc/self/exe" : path,
                         buffer, size);
}
