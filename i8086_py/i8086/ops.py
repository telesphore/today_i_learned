from collections.abc import Callable
from dataclasses import dataclass

OP_MATH1 = " add or adc sbb and sub xor cmp ".split()
OP_MATH2 = " test . not neg mul imul div idiv ".split()
OP_MOVE = " mov . . . . . . . ".split()
OP_STACK = " pop . . . . . . . ".split()
OP_SHIFT = " rol ror rcl rcr sal shr . sar ".split()
OP_OTHER = " inc dec call call jmp jmp push . ".split()


@dataclass
class Op:
    key: int
    fmt: str
    b2: Callable | None = None
    b36: Callable | None = None


def mod_reg_rm():
    pass


def disp():
    pass


def data_lo():
    pass


def data_hi():
    pass


def data8():
    pass


def ip_inc8():
    pass


def ip_inc_lo():
    pass


def ip_inc_hi():
    pass


def mod_op_rm(codes):
    pass


def disp_data8():
    pass


def disp_data16():
    pass


def disp_data_sx():
    pass


def mod_0sr_rm():
    pass


def mod_1xx_rm():
    pass


def disp_hi_seg_lo_seg_hi():
    pass


def disp_lo():
    pass


def addr_lo():
    pass


def addr_hi():
    pass


def literal():
    pass


def mod_yyy_rm():
    pass


def ip_lo():
    pass


def ip_hi_cs_lo_cs_hi():
    pass


# hex binary, b36=2nd_byte	Bytes_3-6	instruction
[
    Op(key=0x00, b2=mod_reg_rm, b36=disp, fmt="add reg8/mem8,reg8"),
    Op(key=0x01, b2=mod_reg_rm, b36=disp, fmt="add reg16/mem16,reg16"),
    Op(key=0x02, b2=mod_reg_rm, b36=disp, fmt="add reg8,reg8/mem8"),
    Op(key=0x03, b2=mod_reg_rm, b36=disp, fmt="add reg16,reg16/mem16"),
    Op(key=0x04, b2=data8, fmt="add al,immed8"),
    Op(key=0x05, b2=data_lo, b36=data_hi, fmt="add ax,immed16"),
    Op(key=0x06, fmt="push es"),
    Op(key=0x07, fmt="pop es"),
    Op(key=0x08, b2=mod_reg_rm, b36=disp, fmt="or reg8/mem8,reg8"),
    Op(key=0x09, b2=mod_reg_rm, b36=disp, fmt="or reg16/mem16,reg16"),
    Op(key=0x0A, b2=mod_reg_rm, b36=disp, fmt="or reg8,reg8/mem8"),
    Op(key=0x0B, b2=mod_reg_rm, b36=disp, fmt="or reg16,reg16/mem16"),
    Op(key=0x0C, b2=data8, fmt="or al,immed8"),
    Op(key=0x0D, b2=data_lo, b36=data_hi, fmt="or ax,immed16"),
    Op(key=0x0E, fmt="push cs"),
    Op(key=0x0F, fmt="(not used)"),
    Op(key=0x10, b2=mod_reg_rm, b36=disp, fmt="adc reg8/mem8,reg8"),
    Op(key=0x11, b2=mod_reg_rm, b36=disp, fmt="adc reg16/mem16,reg16"),
    Op(key=0x12, b2=mod_reg_rm, b36=disp, fmt="adc reg8,reg8/mem8"),
    Op(key=0x13, b2=mod_reg_rm, b36=disp, fmt="adc reg16,reg16/mem16"),
    Op(key=0x14, b2=data8, fmt="adc al,immed8"),
    Op(key=0x15, b2=data_lo, b36=data_hi, fmt="adc ax,immed16"),
    Op(key=0x16, fmt="push ss"),
    Op(key=0x17, fmt="pop ss"),
    Op(key=0x18, b2=mod_reg_rm, b36=disp, fmt="sbb reg8/mem8,reg8"),
    Op(key=0x19, b2=mod_reg_rm, b36=disp, fmt="sbb reg16/mem16,reg16"),
    Op(key=0x1A, b2=mod_reg_rm, b36=disp, fmt="sbb reg8,reg8/mem8"),
    Op(key=0x1B, b2=mod_reg_rm, b36=disp, fmt="sbb reg16,reg16/mem16"),
    Op(key=0x1C, b2=data8, fmt="sbb al,immed8"),
    Op(key=0x1D, b2=data_lo, b36=data_hi, fmt="sbb ax,immed16"),
    Op(key=0x1E, fmt="push ds"),
    Op(key=0x1F, fmt="pop ds"),
    Op(key=0x20, b2=mod_reg_rm, b36=disp, fmt="and reg8/mem8,reg8"),
    Op(key=0x21, b2=mod_reg_rm, b36=disp, fmt="and reg16/mem16,reg16"),
    Op(key=0x22, b2=mod_reg_rm, b36=disp, fmt="and reg8,reg8/mem8"),
    Op(key=0x23, b2=mod_reg_rm, b36=disp, fmt="and reg16,reg16/mem16"),
    Op(key=0x24, b2=data8, fmt="and al,immed8"),
    Op(key=0x25, b2=data_lo, b36=data_hi, fmt="and ax,immed16"),
    Op(key=0x26, fmt="es: (segment override prefix)"),
    Op(key=0x27, fmt="daa"),
    Op(key=0x28, b2=mod_reg_rm, b36=disp, fmt="sub reg8/mem8,reg8"),
    Op(key=0x29, b2=mod_reg_rm, b36=disp, fmt="sub reg16/mem16,reg16"),
    Op(key=0x2A, b2=mod_reg_rm, b36=disp, fmt="sub reg8,reg8/mem8"),
    Op(key=0x2B, b2=mod_reg_rm, b36=disp, fmt="sub reg16,reg16/mem16"),
    Op(key=0x2C, b2=data8, fmt="sub al,immed8"),
    Op(key=0x2D, b2=data_lo, b36=data_hi, fmt="sub ax,immed16"),
    Op(key=0x2E, fmt="cs: (segment override prefix)"),
    Op(key=0x2F, fmt="das"),
    Op(key=0x30, b2=mod_reg_rm, b36=disp, fmt="xor reg8/mem8,reg8"),
    Op(key=0x31, b2=mod_reg_rm, b36=disp, fmt="xor reg16/mem16,reg16"),
    Op(key=0x32, b2=mod_reg_rm, b36=disp, fmt="xor reg8,reg8/mem8"),
    Op(key=0x33, b2=mod_reg_rm, b36=disp, fmt="xor reg16,reg16/mem16"),
    Op(key=0x34, b2=data8, fmt="xor al,immed8"),
    Op(key=0x35, b2=data_lo, b36=data_hi, fmt="xor ax,immed16"),
    Op(key=0x36, fmt="ss: (segment override prefix)"),
    Op(key=0x37, fmt="aaa"),
    Op(key=0x38, b2=mod_reg_rm, b36=disp, fmt="cmp reg8/mem8,reg8"),
    Op(key=0x39, b2=mod_reg_rm, b36=disp, fmt="cmp reg16/mem16,reg16"),
    Op(key=0x3A, b2=mod_reg_rm, b36=disp, fmt="cmp reg8,reg8/mem8"),
    Op(key=0x3B, b2=mod_reg_rm, b36=disp, fmt="cmp reg16,reg16/mem16"),
    Op(key=0x3C, b2=data8, fmt="cmp al,immed8"),
    Op(key=0x3D, b2=data_lo, b36=data_hi, fmt="cmp ax,immed16"),
    Op(key=0x3E, fmt="ds: (segment override prefix)"),
    Op(key=0x3F, fmt="aas"),
    Op(key=0x40, fmt="inc ax"),
    Op(key=0x41, fmt="inc cx"),
    Op(key=0x42, fmt="inc ox"),
    Op(key=0x43, fmt="inc bx"),
    Op(key=0x44, fmt="inc sp"),
    Op(key=0x45, fmt="inc bp"),
    Op(key=0x46, fmt="inc si"),
    Op(key=0x47, fmt="inc di"),
    Op(key=0x48, fmt="dec ax"),
    Op(key=0x49, fmt="dec cx"),
    Op(key=0x4A, fmt="dec ox"),
    Op(key=0x4B, fmt="dec bx"),
    Op(key=0x4C, fmt="dec sp"),
    Op(key=0x4D, fmt="dec bp"),
    Op(key=0x4E, fmt="dec si"),
    Op(key=0x4F, fmt="dec di"),
    Op(key=0x50, fmt="push ax"),
    Op(key=0x51, fmt="push cx"),
    Op(key=0x52, fmt="push ox"),
    Op(key=0x53, fmt="push bx"),
    Op(key=0x54, fmt="push sp"),
    Op(key=0x55, fmt="push bp"),
    Op(key=0x56, fmt="push si"),
    Op(key=0x57, fmt="push di"),
    Op(key=0x58, fmt="pop ax"),
    Op(key=0x59, fmt="pop cx"),
    Op(key=0x5A, fmt="pop dx"),
    Op(key=0x5B, fmt="pop bx"),
    Op(key=0x5C, fmt="pop sp"),
    Op(key=0x5D, fmt="pop bp"),
    Op(key=0x5E, fmt="pop si"),
    Op(key=0x5F, fmt="pop di"),
    Op(key=0x60, fmt="(not used)"),
    Op(key=0x61, fmt="(not used)"),
    Op(key=0x62, fmt="(not used)"),
    Op(key=0x63, fmt="(not used)"),
    Op(key=0x64, fmt="(not used)"),
    Op(key=0x65, fmt="(not used)"),
    Op(key=0x66, fmt="(not used)"),
    Op(key=0x67, fmt="(not used)"),
    Op(key=0x68, fmt="(not used)"),
    Op(key=0x69, fmt="(not used)"),
    Op(key=0x6A, fmt="(not used)"),
    Op(key=0x6B, fmt="(not used)"),
    Op(key=0x6C, fmt="(not used)"),
    Op(key=0x6D, fmt="(not used)"),
    Op(key=0x6E, fmt="(not used)"),
    Op(key=0x6F, fmt="(not used)"),
    Op(key=0x70, b2=ip_inc8, fmt="jo short-label"),
    Op(key=0x71, b2=ip_inc8, fmt="jno short-label"),
    Op(key=0x72, b2=ip_inc8, fmt="jb/jnaei short-label jc"),
    Op(key=0x73, b2=ip_inc8, fmt="jnb/jaei short-label jnc"),
    Op(key=0x74, b2=ip_inc8, fmt="je/jz short-label"),
    Op(key=0x75, b2=ip_inc8, fmt="jne/jnz short-label"),
    Op(key=0x76, b2=ip_inc8, fmt="jbe/jna short-label"),
    Op(key=0x77, b2=ip_inc8, fmt="jnbe/ja short-label"),
    Op(key=0x78, b2=ip_inc8, fmt="js short-label"),
    Op(key=0x79, b2=ip_inc8, fmt="jns short-label"),
    Op(key=0x7A, b2=ip_inc8, fmt="jp/jpe short-label"),
    Op(key=0x7B, b2=ip_inc8, fmt="jnp/jpo short-label"),
    Op(key=0x7C, b2=ip_inc8, fmt="jlljnge short-label"),
    Op(key=0x7D, b2=ip_inc8, fmt="jnlljge short-label"),
    Op(key=0x7E, b2=ip_inc8, fmt="jle/jng short-label"),
    Op(key=0x7F, b2=ip_inc8, fmt="jnle/jg short-label"),
    Op(key=0x80, b2=mod_op_rm(OP_MATH1), b36=disp_data8, fmt="add reg8/mem8,immed8"),
    Op(
        key=0x81,
        b2=mod_op_rm(OP_MATH1),
        b36=disp_data16,
        fmt="add reg16/mem16,immed16",
    ),
    Op(key=0x82, b2=mod_op_rm(OP_MATH1), b36=disp_data8, fmt="add reg8/mem8,immed8"),
    Op(
        key=0x83, b2=mod_op_rm(OP_MATH1), b36=disp_data_sx, fmt="add reg16/mem16,immed8"
    ),
    Op(key=0x84, b2=mod_reg_rm, b36=disp, fmt="test reg8/mem8,reg8"),
    Op(key=0x85, b2=mod_reg_rm, b36=disp, fmt="test reg16/mem16,reg16"),
    Op(key=0x86, b2=mod_reg_rm, b36=disp, fmt="xchg reg8,reg8/mem8"),
    Op(key=0x87, b2=mod_reg_rm, b36=disp, fmt="xchg reg16,reg16/mem16"),
    Op(key=0x88, b2=mod_reg_rm, b36=disp, fmt="mov reg81 m em8,reg8"),
    Op(key=0x89, b2=mod_reg_rm, b36=disp, fmt="mov reg16/mem16/reg16"),
    Op(key=0x8A, b2=mod_reg_rm, b36=disp, fmt="mov reg8,reg8/mem8"),
    Op(key=0x8B, b2=mod_reg_rm, b36=disp, fmt="mov reg16,reg16/mem16"),
    Op(key=0x8C, b2=mod_0sr_rm, b36=disp, fmt="mov reg16/mem16,segreg"),
    Op(key=0x8C, b2=mod_1xx_rm, fmt="(not used)"),
    Op(key=0x8D, b2=mod_reg_rm, b36=disp, fmt="lea reg16,mem16"),
    Op(key=0x8E, b2=mod_0sr_rm, b36=disp, fmt="mov segreg,reg16/mem16"),
    Op(key=0x8F, b2=mod_op_rm(OP_STACK), b36=disp, fmt="pop reg16/mem16"),
    Op(key=0x90, fmt="nop (exchange ax,ax)"),
    Op(key=0x91, fmt="xchg ax,cx"),
    Op(key=0x92, fmt="xchg ax,dx"),
    Op(key=0x93, fmt="xchg ax,bx"),
    Op(key=0x94, fmt="xchg ax,sp"),
    Op(key=0x95, fmt="xchg ax,bp"),
    Op(key=0x96, fmt="xchg ax,si"),
    Op(key=0x97, fmt="xchg ax,di"),
    Op(key=0x98, fmt="cbw"),
    Op(key=0x99, fmt="cwd"),
    Op(key=0x9A, b2=disp_lo, b36=disp_hi_seg_lo_seg_hi, fmt="call far_proc"),
    Op(key=0x9B, fmt="wait"),
    Op(key=0x9C, fmt="pushf"),
    Op(key=0x9D, fmt="popf"),
    Op(key=0x9E, fmt="sahf"),
    Op(key=0x9F, fmt="lahf"),
    Op(key=0xA0, b2=addr_lo, b36=addr_hi, fmt="mov al,mem8"),
    Op(key=0xA1, b2=addr_lo, b36=addr_hi, fmt="mov ax,mem16"),
    Op(key=0xA2, b2=addr_lo, b36=addr_hi, fmt="mov mem8,al"),
    Op(key=0xA3, b2=addr_lo, b36=addr_hi, fmt="mov mem16,al"),
    Op(key=0xA4, fmt="movs dest-str8,src-str8"),
    Op(key=0xA5, fmt="movs dest-str16,src-str16"),
    Op(key=0xA6, fmt="cmps dest-str8,src-str8"),
    Op(key=0xA7, fmt="cmps dest-str16,src-str16"),
    Op(key=0xA8, b2=data8, fmt="test al,immed8"),
    Op(key=0xA9, b2=data_lo, b36=data_hi, fmt="test ax,immed16"),
    Op(key=0xAA, fmt="stos dest-str8"),
    Op(key=0xAB, fmt="stos dest-str16"),
    Op(key=0xAC, fmt="lods src-str8"),
    Op(key=0xAD, fmt="lods src-str16"),
    Op(key=0xAE, fmt="scas dest-str8"),
    Op(key=0xAF, fmt="scas dest-str16"),
    Op(key=0xB0, b2=data8, fmt="mov al,immed8"),
    Op(key=0xB1, b2=data8, fmt="mov cl,immed8"),
    Op(key=0xB2, b2=data8, fmt="mov dl,immed8"),
    Op(key=0xB3, b2=data8, fmt="mov bl,immed8"),
    Op(key=0xB4, b2=data8, fmt="mov ah,immed8"),
    Op(key=0xB5, b2=data8, fmt="mov ch,immed8"),
    Op(key=0xB6, b2=data8, fmt="mov dh,immed8"),
    Op(key=0xB7, b2=data8, fmt="mov bh,immed8"),
    Op(key=0xB8, b2=data_lo, b36=data_hi, fmt="mov ax,immed16"),
    Op(key=0xB9, b2=data_lo, b36=data_hi, fmt="mov cx,immed16"),
    Op(key=0xBA, b2=data_lo, b36=data_hi, fmt="mov dx,immed16"),
    Op(key=0xBB, b2=data_lo, b36=data_hi, fmt="mov bx,immed16"),
    Op(key=0xBC, b2=data_lo, b36=data_hi, fmt="mov sp,immed16"),
    Op(key=0xBD, b2=data_lo, b36=data_hi, fmt="mov bp,immed16"),
    Op(key=0xBE, b2=data_lo, b36=data_hi, fmt="mov si,immed16"),
    Op(key=0xBF, b2=data_lo, b36=data_hi, fmt="mov di,immed16"),
    Op(key=0xC0, fmt="(not used)"),
    Op(key=0xC1, fmt="(not used)"),
    Op(key=0xC2, b2=data_lo, b36=data_hi, fmt="ret immed16 (intraseg)"),
    Op(key=0xC3, fmt="ret (intrasegment)"),
    Op(key=0xC4, b2=mod_reg_rm, b36=disp, fmt="les reg16,mem16"),
    Op(key=0xC5, b2=mod_reg_rm, b36=disp, fmt="lds reg16,mem16"),
    Op(key=0xC6, b2=mod_op_rm(OP_MOVE), b36=disp_data8, fmt="mov mem8,immed8"),
    Op(key=0xC7, b2=mod_op_rm(OP_MOVE), b36=disp_data16, fmt="mov mem16,immed16"),
    Op(key=0xC8, fmt="(not used)"),
    Op(key=0xC9, fmt="(not used)"),
    Op(key=0xCA, b2=data_lo, b36=data_hi, fmt="ret immed16 (intersegment)"),
    Op(key=0xCB, fmt="ret (intersegment)"),
    Op(key=0xCC, fmt="int 3"),
    Op(key=0xCD, b2=data8, fmt="int immed8"),
    Op(key=0xCE, fmt="into"),
    Op(key=0xCF, fmt="iret"),
    Op(key=0xD0, b2=mod_op_rm(OP_SHIFT), b36=disp, fmt="rol reg8/mem8,1"),
    Op(key=0xD1, b2=mod_op_rm(OP_SHIFT), b36=disp, fmt="rol reg16/mem16,1"),
    Op(key=0xD2, b2=mod_op_rm(OP_SHIFT), b36=disp, fmt="rol reg8/mem8,cl"),
    Op(key=0xD3, b2=mod_op_rm(OP_SHIFT), b36=disp, fmt="rol reg16/mem16,cl"),
    Op(key=0xD4, b2=literal(1010), fmt="aam"),
    Op(key=0xD5, b2=literal(1010), fmt="aad"),
    Op(key=0xD6, fmt="(not used)"),
    Op(key=0xD7, fmt="xlat source-table"),
    Op(key=0xD8, b2=mod_yyy_rm, fmt="?"),
    Op(key=0xD9, b2=mod_yyy_rm, b36=disp, fmt="esc opcode,source"),
    Op(key=0xDA, b2=mod_yyy_rm, b36=disp, fmt="esc opcode,source"),
    Op(key=0xDB, b2=mod_yyy_rm, b36=disp, fmt="esc opcode,source"),
    Op(key=0xDC, b2=mod_yyy_rm, b36=disp, fmt="esc opcode,source"),
    Op(key=0xDD, b2=mod_yyy_rm, b36=disp, fmt="esc opcode,source"),
    Op(key=0xDE, b2=mod_yyy_rm, b36=disp, fmt="esc opcode,source"),
    Op(key=0xDF, b2=mod_yyy_rm, fmt="?"),
    Op(key=0xE0, b2=ip_inc8, fmt="loopne/loopnz short-label"),
    Op(key=0xE1, b2=ip_inc8, fmt="loopeloopz short-label"),
    Op(key=0xE2, b2=ip_inc8, fmt="loop short-label"),
    Op(key=0xE3, b2=ip_inc8, fmt="jcxz short~label"),
    Op(key=0xE4, b2=data8, fmt="in al,immed8"),
    Op(key=0xE5, b2=data8, fmt="in ax,immed8"),
    Op(key=0xE6, b2=data8, fmt="out al,immed8"),
    Op(key=0xE7, b2=data8, fmt="out ax,immed8"),
    Op(key=0xE8, b2=ip_inc_lo, b36=ip_inc_hi, fmt="call near-proc"),
    Op(key=0xE9, b2=ip_inc_lo, b36=ip_inc_hi, fmt="jmp near-label"),
    Op(key=0xEA, b2=ip_lo, b36=ip_hi_cs_lo_cs_hi, fmt="jmp far-label"),
    Op(key=0xEB, b2=ip_inc8, fmt="jmp short-label"),
    Op(key=0xEC, fmt="in al,dx"),
    Op(key=0xED, fmt="in ax,dx"),
    Op(key=0xEE, fmt="out al,dx"),
    Op(key=0xEF, fmt="out ax,dx"),
    Op(key=0xF0, fmt="lock (prefix)"),
    Op(key=0xF1, fmt="(not used)"),
    Op(key=0xF2, fmt="repne/repnz"),
    Op(key=0xF3, fmt="rep/repe/rerz"),
    Op(key=0xF4, fmt="hlt"),
    Op(key=0xF5, fmt="cmc"),
    Op(key=0xF6, b2=mod_op_rm(OP_MATH2), b36=disp_data8, fmt="test reg8/mem8,immed8"),
    Op(
        key=0xF7,
        b2=mod_op_rm(OP_MATH2),
        b36=disp_data16,
        fmt="test reg16/mem16,immed16",
    ),
    Op(key=0xF8, fmt="clc"),
    Op(key=0xF9, fmt="stc"),
    Op(key=0xFA, fmt="cli"),
    Op(key=0xFB, fmt="sti"),
    Op(key=0xFC, fmt="cld"),
    Op(key=0xFD, fmt="std"),
    Op(key=0xFE, b2=mod_op_rm(OP_OTHER), b36=disp, fmt="inc reg8/mem8"),
    Op(key=0xFF, b2=mod_op_rm(OP_OTHER), b36=disp, fmt="inc mem16"),
]
