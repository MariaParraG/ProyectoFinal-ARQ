from cpu.isa import Instruction
from memory.cache import DirectMappedCache
from io.device import FakeIODevice
from io.interrupt import InterruptController

class PipelineStage:
    def __init__(self, name):
        self.name = name
        self.instr = None

class Pipeline:
    def __init__(self):
        self.IF = PipelineStage("IF")
        self.ID = PipelineStage("ID")
        self.EX = PipelineStage("EX")
        self.MEM = PipelineStage("MEM")
        self.WB = PipelineStage("WB")
        self.registers = {f"R{i}": 0 for i in range(8)}
        self.pc = 0
        self.instruction_memory = []
        self.clock = 0
        self.memory = {}
        self.labels = {}
        self.cache = DirectMappedCache(size=8)
        self.io_device = FakeIODevice()
        self.interrupts = InterruptController()

    def load_program(self, instrucciones_etiquetas):
        instrucciones, etiquetas = instrucciones_etiquetas
        self.instruction_memory = instrucciones
        self.labels = etiquetas

    def flush_pipeline(self):
        self.IF.instr = None
        self.ID.instr = None

    def detect_data_hazard(self):
        if not self.ID.instr or not self.EX.instr:
            return False
        write_reg = self.EX.instr.rd
        if self.EX.instr.opcode in ["ADD", "SUB", "MUL", "LOAD"] and write_reg:
            read_regs = [self.ID.instr.rs1, self.ID.instr.rs2]
            if write_reg in read_regs:
                return True
        return False

    def execute_instruction(self, instr: Instruction):
        if instr.opcode == "ADD":
            self.registers[instr.rd] = self.registers[instr.rs1] + self.registers[instr.rs2]
        elif instr.opcode == "SUB":
            self.registers[instr.rd] = self.registers[instr.rs1] - self.registers[instr.rs2]
        elif instr.opcode == "MUL":
            self.registers[instr.rd] = self.registers[instr.rs1] * self.registers[instr.rs2]
        elif instr.opcode == "LOAD":
            addr = self.registers[instr.rs1] + instr.imm
            self.registers[instr.rd] = self.cache.read(addr)
        elif instr.opcode == "STORE":
            addr = self.registers[instr.rs1] + instr.imm
            self.cache.write(addr, self.registers[instr.rd])
        elif instr.opcode == "BEQ":
            if self.registers[instr.rs1] == self.registers[instr.rs2]:
                self.pc = self.labels.get(instr.label, self.pc)
                self.flush_pipeline()
        elif instr.opcode == "JUMP":
            self.pc = self.labels.get(instr.label, self.pc)
            self.flush_pipeline()

    def cycle(self):
        self.clock += 1
        print(f"\n[Ciclo {self.clock}]")

        if self.clock == 3:
            self.io_device.push_data(42)
            self.interrupts.trigger()

        if self.interrupts.is_pending():
            print("[INTERRUPCIÓN] leyendo del dispositivo...")
            data = self.io_device.read()
            self.registers["R7"] = data
            self.interrupts.clear()
            self.flush_pipeline()
            return

        hazard = self.detect_data_hazard()
        if hazard:
            print("[STALL DETECTADO]")
            self.WB.instr = self.MEM.instr
            self.MEM.instr = self.EX.instr
            self.EX.instr = None
        else:
            self.WB.instr = self.MEM.instr
            self.MEM.instr = self.EX.instr
            self.EX.instr = self.ID.instr
            self.ID.instr = self.IF.instr
            if self.pc < len(self.instruction_memory):
                self.IF.instr = self.instruction_memory[self.pc]
                self.pc += 1
            else:
                self.IF.instr = None

        if self.EX.instr and self.MEM.instr:
            ex = self.EX.instr
            mem = self.MEM.instr
            if mem.opcode in ["ADD", "SUB", "MUL", "LOAD"]:
                if ex.rs1 == mem.rd:
                    self.registers[ex.rs1] = self.registers[mem.rd]
                if ex.rs2 == mem.rd:
                    self.registers[ex.rs2] = self.registers[mem.rd]

        for stage in [self.IF, self.ID, self.EX, self.MEM, self.WB]:
            print(f"{stage.name}: {stage.instr}")
        if not hazard and self.EX.instr:
            self.execute_instruction(self.EX.instr)
