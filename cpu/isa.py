from dataclasses import dataclass

@dataclass
class Instruction:
    opcode: str
    rd: str = ""
    rs1: str = ""
    rs2: str = ""
    imm: int = 0
    label: str = ""

def parse_instruction(line: str) -> Instruction:
    tokens = line.strip().split()
    if not tokens:
        return None

    opcode = tokens[0].upper()
    args = tokens[1:] if len(tokens) > 1 else []

    if opcode in ["ADD", "SUB", "MUL"]:
        rd, rs1, rs2 = [arg.strip() for arg in args[0].split(',')]
        return Instruction(opcode, rd, rs1, rs2)
    elif opcode in ["LOAD", "STORE"]:
        rd, mem = args[0].split(',')
        offset, rs1 = mem.strip().strip(')').split('(')
        return Instruction(opcode, rd, rs1, imm=int(offset))
    elif opcode == "BEQ":
        rs1, rs2, label = [arg.strip() for arg in args[0].split(',')]
        return Instruction(opcode, rs1=rs1, rs2=rs2, label=label)
    elif opcode == "JUMP":
        return Instruction(opcode, label=args[0].strip())
    else:
        raise ValueError(f"Instrucción no válida: {opcode}")

def procesar_con_etiquetas(lines: list[str]):
    instrucciones = []
    etiquetas = {}
    contador = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            label, instr = line.split(":")
            etiquetas[label.strip()] = contador
            if instr.strip():
                instrucciones.append(parse_instruction(instr.strip()))
                contador += 1
        else:
            instrucciones.append(parse_instruction(line))
            contador += 1

    return instrucciones, etiquetas
