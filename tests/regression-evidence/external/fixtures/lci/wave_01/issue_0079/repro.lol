 RAX  0x37600000
 RBX  0x0
 RCX  0x5555555e8376 ◂— 0x5754420052444c54 /* 'TLDR' */
 RDX  0x4
 RDI  0x5555556f8000
 RSI  0x5555555e8376 ◂— 0x5754420052444c54 /* 'TLDR' */
 R8   0x0
 R9   0x0
 R10  0x8a7732fc159aa867
 R11  0x7ffff7ebbc60 (main_arena) ◂— 0x0
 R12  0x7fffffffde98 —▸ 0x7fffffffe216 ◂— '/dev/shm/lci/lci'
 R13  0x5555555e100b (main) ◂— push   rbp
 R14  0x5555556aade0 (__do_global_dtors_aux_fini_array_entry) —▸ 0x5555555da2e0 (__do_global_dtors_aux) ◂— endbr64 
 R15  0x7ffff7ffd020 (_rtld_global) —▸ 0x7ffff7ffe2c0 —▸ 0x555555554000 ◂— 0x10102464c457f
 RBP  0x7fffffffdd10 —▸ 0x7fffffffdd80 ◂— 0x2
 RSP  0x7fffffffdc88 —▸ 0x5555555e0a44 (scanBuffer+1437) ◂— test   eax, eax
 RIP  0x7ffff7e2046d (__strncmp_avx2+29) ◂— vmovdqu ymm0, ymmword ptr [rdi]
──────────────────────────────────────────────────────────────────────────────────────────────────[ DISASM ]──────────────────────────────────────────────────────────────────────────────────────────────────
 ► 0x7ffff7e2046d <__strncmp_avx2+29>    vmovdqu ymm0, ymmword ptr [rdi]
   0x7ffff7e20471 <__strncmp_avx2+33>    vpcmpeqb ymm1, ymm0, ymmword ptr [rsi]
   0x7ffff7e20475 <__strncmp_avx2+37>    vpcmpeqb ymm2, ymm15, ymm0
   0x7ffff7e20479 <__strncmp_avx2+41>    vpandn ymm1, ymm2, ymm1
   0x7ffff7e2047d <__strncmp_avx2+45>    vpmovmskb ecx, ymm1
   0x7ffff7e20481 <__strncmp_avx2+49>    cmp    rdx, 0x20
   0x7ffff7e20485 <__strncmp_avx2+53>    jbe    __strncmp_avx2+80                <__strncmp_avx2+80>
    ↓
   0x7ffff7e204a0 <__strncmp_avx2+80>    not    ecx
   0x7ffff7e204a2 <__strncmp_avx2+82>    bzhi   eax, ecx, edx
   0x7ffff7e204a7 <__strncmp_avx2+87>    jne    __strncmp_avx2+59                <__strncmp_avx2+59>
    ↓
   0x7ffff7e2048b <__strncmp_avx2+59>    tzcnt  ecx, ecx
──────────────────────────────────────────────────────────────────────────────────────────────────[ STACK ]───────────────────────────────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7fffffffdc88 —▸ 0x5555555e0a44 (scanBuffer+1437) ◂— test   eax, eax
01:0008│     0x7fffffffdc90 —▸ 0x5555556d7480 ◂— 0x5555556d7
02:0010│     0x7fffffffdc98 —▸ 0x7fffffffe227 ◂— 'vuln/overflow.lo'
03:0018│     0x7fffffffdca0 ◂— 0x24400000000
04:0020│     0x7fffffffdca8 —▸ 0x5555556d86a0 ◂— 0xa322e3120494148 ('HAI 1.2\n')
05:0028│     0x7fffffffdcb0 —▸ 0x5555555e100b (main) ◂— push   rbp
06:0030│     0x7fffffffdcb8 —▸ 0x5555556aade0 (__do_global_dtors_aux_fini_array_entry) —▸ 0x5555555da2e0 (__do_global_dtors_aux) ◂— endbr64 
07:0038│     0x7fffffffdcc0 —▸ 0x5555556d7a90 —▸ 0x5555556d7ba0 —▸ 0x7ffff7eb0021 ◂— 0x38000b42080e4210
────────────────────────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]─────────────────────────────────────────────────────────────────────────────────────────────────
 ► f 0   0x7ffff7e2046d __strncmp_avx2+29
   f 1   0x5555555e0a44 scanBuffer+1437
   f 2   0x5555555e1394 main+905
   f 3   0x7ffff7cf020a __libc_start_call_main+122
   f 4   0x7ffff7cf02bc __libc_start_main+124
   f 5   0x5555555da261 _start+33

