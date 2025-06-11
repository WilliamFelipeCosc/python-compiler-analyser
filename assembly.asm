.data
menu1:      .asciiz "\nInsira o tipo de juros:\n1 - Juros Simples\n2 - Juros Compostos\nDigite 1 ou 2: "
inv_op:     .asciiz "\nOpcao invalida. Digite 1 ou 2.\n"
cap_msg:    .asciiz "\nDigite o capital (R$): "
taxa_msg:   .asciiz "Digite a taxa de juros (%): "
tempo_msg:  .asciiz "Digite o tempo (em meses): "
neg_msg:    .asciiz "\nOs valores devem ser positivos.\n"
js_msg:     .asciiz "\nJuros Simples: R$ "
jc_msg:     .asciiz "\nJuros Compostos: R$ "
mont_msg:   .asciiz "\nMontante: R$ "
newline:    .asciiz "\n"

.text
.globl main

main:
    # Menu de seleção
menu_loop:
    li $v0, 4
    la $a0, menu1
    syscall

    li $v0, 5
    syscall
    move $t0, $v0         # $t0 = tipo_juros

    li $t1, 1
    li $t2, 2
    beq $t0, $t1, input_values
    beq $t0, $t2, input_values

    # Opção inválida
    li $v0, 4
    la $a0, inv_op
    syscall
    j menu_loop

input_values:
    # Entrada do capital
    li $v0, 4
    la $a0, cap_msg
    syscall
    li $v0, 6
    syscall
    mov.s $f2, $f0        # $f2 = capital

    # Entrada da taxa
    li $v0, 4
    la $a0, taxa_msg
    syscall
    li $v0, 6
    syscall
    mov.s $f4, $f0        # $f4 = taxa

    # Entrada do tempo
    li $v0, 4
    la $a0, tempo_msg
    syscall
    li $v0, 5
    syscall
    move $t3, $v0         # $t3 = tempo (int)

    # Checagem de valores negativos
    # li.s $f12, 0.0
    # Substituir por:
    li $t4, 0x00000000       # 0.0 em IEEE 754
    mtc1 $t4, $f12

    c.lt.s $f2, $f12
    bc1t neg_value
    c.lt.s $f4, $f12
    bc1t neg_value
    bltz $t3, neg_value

    # Calculo dos juros
    beq $t0, $t1, juros_simples
    beq $t0, $t2, juros_compostos

juros_simples:
    # juros = capital * (taxa / 100) * tempo
    # li.s $f6, 100.0
    li $t4, 0x42c80000       # 100.0 em IEEE 754
    mtc1 $t4, $f6

    div.s $f8, $f4, $f6       # $f8 = taxa / 100
    mul.s $f10, $f2, $f8      # $f10 = capital * (taxa / 100)
    mtc1 $t3, $f16
    cvt.s.w $f16, $f16        # $f16 = float(tempo)
    mul.s $f12, $f10, $f16    # $f12 = juros simples

    # montante = capital + juros
    add.s $f14, $f2, $f12     # $f14 = montante

    # Exibe resultado
    li $v0, 4
    la $a0, js_msg
    syscall
    li $v0, 2
    mov.s $f12, $f12
    syscall

    li $v0, 4
    la $a0, mont_msg
    syscall
    li $v0, 2
    mov.s $f12, $f14
    syscall

    li $v0, 4
    la $a0, newline
    syscall
    j fim

juros_compostos:
    # montante = capital * (1 + taxa/100) ** tempo
    # li.s $f6, 100.0
    li $t4, 0x42c80000       # 100.0 em IEEE 754
    mtc1 $t4, $f6

    div.s $f8, $f4, $f6       # $f8 = taxa / 100
    # li.s $f10, 1.0
    li $t4, 0x3f800000       # 1.0 em IEEE 754
    mtc1 $t4, $f10

    add.s $f10, $f10, $f8     # $f10 = 1 + taxa/100

    mtc1 $t3, $f16
    cvt.s.w $f16, $f16        # $f16 = float(tempo)

    # powf: $f18 = ($f10) ** ($f16)
    # MARS tem syscall 43 para pow
    mov.s $f12, $f10
    mov.s $f13, $f16
    li $v0, 43
    syscall
    mov.s $f18, $f0           # $f18 = (1 + taxa/100) ** tempo

    mul.s $f14, $f2, $f18     # $f14 = montante

    # juros = montante - capital
    sub.s $f12, $f14, $f2     # $f12 = juros compostos

    # Exibe resultado
    li $v0, 4
    la $a0, jc_msg
    syscall
    li $v0, 2
    mov.s $f12, $f12
    syscall

    li $v0, 4
    la $a0, mont_msg
    syscall
    li $v0, 2
    mov.s $f12, $f14
    syscall

    li $v0, 4
    la $a0, newline
    syscall
    j fim

neg_value:
    li $v0, 4
    la $a0, neg_msg
    syscall
    j input_values

fim:
    li $v0, 10
    syscall