/*
 * Explicit application-path adapter for the official Lean 4.34.1 binary.
 *
 * Some execution hosts do not expose /proc/<pid>/exe. Lean's IO.appPath
 * queries that path during search-path initialization, before command-line
 * processing. For that exact own-process query this adapter copies an
 * explicitly configured application path, without making a filesystem
 * access. Other readlink calls retain the host's original behavior.
 * It does not modify Lean's kernel, alter any theorem, replace a
 * proof-checking function, or change the release binary.
 *
 * Omit this adapter on an ordinary host where Lean starts normally.
 */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buffer, size_t size) {
    char own_executable[64];
    snprintf(own_executable, sizeof own_executable, "/proc/%d/exe",
             (int)getpid());
    if (strcmp(path, own_executable) == 0) {
        const char *configured = getenv("STRUCT2_LEAN_BIN");
        if (configured == NULL || configured[0] == '\0') {
            errno = EINVAL;
            return -1;
        }
        size_t length = strlen(configured);
        if (length > size)
            length = size;
        memcpy(buffer, configured, length);
        return (ssize_t)length;
    }
    typedef ssize_t (*readlink_fn)(const char *, char *, size_t);
    readlink_fn original = (readlink_fn)dlsym(RTLD_NEXT, "readlink");
    if (original == NULL) {
        errno = ENOSYS;
        return -1;
    }
    return original(path, buffer, size);
}
