#include <time.h>
#include <stdio.h>

/* https://linux.die.net/man/2/clock_gettime */

int main()
{
    struct timespec mono_raw, boottime, realtime, boottime_inv, realtime_inv;
    long long delta, delta_inv, min_delta_avg;
    //clock_gettime(CLOCK_MONOTONIC_RAW, &mono_raw);
    int i;
    //long long array_delta[10];
    long long min_delta = 0;
    long long min_delta_inv = 0;
    //long long max_delta;
    for (i=0;i<9;i++) {
      clock_gettime(CLOCK_BOOTTIME, &boottime);
      clock_gettime(CLOCK_REALTIME, &realtime);

      clock_gettime(CLOCK_REALTIME, &realtime_inv);
      clock_gettime(CLOCK_BOOTTIME, &boottime_inv);

      //printf("boottime: %lld.%ld\n", (long long) boottime.tv_sec, boottime.tv_nsec);
      //printf("realtime: %lld.%ld\n", (long long) realtime.tv_sec, realtime.tv_nsec);
      delta =  realtime.tv_sec * 1000000000 + realtime.tv_nsec - boottime.tv_sec * 1000000000 - boottime.tv_nsec;
      delta_inv =  realtime_inv.tv_sec * 1000000000 + realtime_inv.tv_nsec - boottime_inv.tv_sec * 1000000000 - boottime_inv.tv_nsec;
      //printf("delta: %lld\n", delta);
      //printf("delta s: %lld\n", delta/1000000000);
      //printf("delta ns: %lld\n", delta%1000000000);
      //printf("delta_inv ns: %lld\n", delta%1000000000);
      if (min_delta== 0) {
         min_delta = delta;
      } else {
        if (delta < min_delta) {
           min_delta = delta;
        }
      }
      if (min_delta_inv== 0) {
         min_delta_inv = delta_inv;
      } else {
        if (delta_inv < min_delta_inv) {
           min_delta_inv = delta_inv;
        }
      }
    }
    min_delta_avg = (min_delta + min_delta_inv) / 2;
    //printf("min_delta: %lld\n", min_delta);
    //printf("min_delta s: %lld\n", min_delta/1000000000);
   //  printf("min_delta ns    : %lld\n", min_delta%1000000000);
    //printf("min_delta_inv: %lld\n", min_delta_inv);
    //printf("min_delta_inv s: %lld\n", min_delta_inv/1000000000);
   //  printf("min_delta_inv ns: %lld\n", min_delta_inv%1000000000);
    printf("%lld\n", min_delta_avg);

}
