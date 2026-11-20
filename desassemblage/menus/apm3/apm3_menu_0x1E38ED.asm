; apm3_menu_0x1E38ED
;
; Cible   : vf5fs-pxd-w64-Retail_APM3.dll (module d APM3)
; Adresse : 0x1E38ED  (80 instructions demandees)
; A quoi  : la sequence de menu d APM3 : temoin 0x5140C -> &+0x29E8 -> commande 74
;
; Desassemblage par VF5RE/oracle_desassembler.py, vide le 2026-11-07.
; Le PE n est ni charge ni execute : on lit le fichier.
; CE N EST PAS DU CODE A RECOPIER : c est une LECTURE, gardee pour ne pas la refaire.
;
oracle  : vf5fs-pxd-w64-Retail_APM3.dll  (6965248 octets)
base PE : 0x180000000
cible   : 0x1801E38ED   (RVA 0x1E38ED, section .text, offset 0x1E2CED)

  0001801E38ED  C7 83 E8 29 00 00 0C 14  mov      dword ptr [rbx + 0x29e8], 0x5140c
  0001801E38F7  66 89 B3 EC 29 00 00     mov      word ptr [rbx + 0x29ec], si
  0001801E38FE  40 88 B3 EE 29 00 00     mov      byte ptr [rbx + 0x29ee], sil
  0001801E3905  48 89 B3 F0 29 00 00     mov      qword ptr [rbx + 0x29f0], rsi
  0001801E390C  48 89 B3 50 06 00 00     mov      qword ptr [rbx + 0x650], rsi
  0001801E3913  48 8B 05 D6 7D A5 00     mov      rax, qword ptr [rip + 0xa57dd6]
  0001801E391A  48 85 C0                 test     rax, rax
  0001801E391D  0F 84 1C 05 00 00        je       0x1801e3e3f
  0001801E3923  48 39 B0 10 FE 01 00     cmp      qword ptr [rax + 0x1fe10], rsi
  0001801E392A  0F 84 0F 05 00 00        je       0x1801e3e3f
  0001801E3930  48 8D 8B 00 2A 00 00     lea      rcx, [rbx + 0x2a00]
  0001801E3937  E8 44 F5 FF FF           call     0x1801e2e80   -> RVA 0x1E2E80 (.text)
  0001801E393C  45 33 C0                 xor      r8d, r8d
  0001801E393F  48 8D 15 6A F2 34 00     lea      rdx, [rip + 0x34f26a]
  0001801E3946  33 C9                    xor      ecx, ecx
  0001801E3948  E8 53 24 FA FF           call     0x180185da0   -> RVA 0x185DA0 (.text)
  0001801E394D  48 8B 0D 9C 7D A5 00     mov      rcx, qword ptr [rip + 0xa57d9c]
  0001801E3954  48 8B 81 10 FE 01 00     mov      rax, qword ptr [rcx + 0x1fe10]
  0001801E395B  48 85 C0                 test     rax, rax
  0001801E395E  0F 84 DB 04 00 00        je       0x1801e3e3f
  0001801E3964  48 8B 89 18 FE 01 00     mov      rcx, qword ptr [rcx + 0x1fe18]
  0001801E396B  4C 8D 83 E8 29 00 00     lea      r8, [rbx + 0x29e8]
  0001801E3972  BA 4A 00 00 00           mov      edx, 0x4a
  0001801E3977  FF D0                    call     rax
  0001801E3979  83 F8 01                 cmp      eax, 1
  0001801E397C  0F 85 BD 04 00 00        jne      0x1801e3e3f
  0001801E3982  40 38 B3 FB 29 00 00     cmp      byte ptr [rbx + 0x29fb], sil
  0001801E3989  0F 84 B0 02 00 00        je       0x1801e3c3f
  0001801E398F  48 8B 0D 5A 66 22 00     mov      rcx, qword ptr [rip + 0x22665a]
  0001801E3996  E8 35 3A FB FF           call     0x1801973d0   -> RVA 0x1973D0 (.text)
  0001801E399B  B0 01                    mov      al, 1
  0001801E399D  E9 9F 04 00 00           jmp      0x1801e3e41   -> RVA 0x1E3E41 (.text)
  --- `jmp` inconditionnel : le gestionnaire s'arrete ici (sortie commune). `--jmp` pour continuer quand meme. ---
