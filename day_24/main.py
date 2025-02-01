from collections import defaultdict
from enum import Enum
from operator import xor, and_, or_
from pathlib import Path
from typing import Literal

from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen


class Gate(Enum):
    AND = and_
    XOR = xor
    OR = or_


def solve(path: Path) -> None:
    initial_wires, circuit = path.read_text().strip().split("\n\n")

    known_wires: dict[str, bool] = {}
    unsolved_gates: dict[tuple[str, str], list[tuple[Gate, str]]] = defaultdict(list)

    for line in initial_wires.splitlines():
        wire, value = line.split(": ")
        known_wires[wire] = True if value == "1" else False

    for line in circuit.splitlines():
        left, out_wire = line.split(" -> ")
        in_wire_1, gate_name, in_wire_2 = left.split(" ")
        unsolved_gates[tuple(sorted([in_wire_1, in_wire_2]))].append((Gate[gate_name], out_wire))

    while len(unsolved_gates) != 0:
        indices_to_remove = []
        for in_gates, out_gates in unsolved_gates.items():
            if in_gates[0] in known_wires and in_gates[1] in known_wires:
                for gate, out_wire in out_gates:
                    known_wires[out_wire] = gate.value(known_wires[in_gates[0]], known_wires[in_gates[1]])

                indices_to_remove.append(in_gates)

        for index_to_remove in indices_to_remove:
            unsolved_gates.pop(index_to_remove)

    z = calculate_decimal("z", known_wires)
    solution_part_1 = z
    print(solution_part_1)

    x = calculate_decimal("x", known_wires)
    print(f"{x=}")
    y = calculate_decimal("y", known_wires)
    print(f"{y=}")
    z_expected = x+y
    print(f"x+y : {z_expected:b}")
    print(f"z   : {z:b}")
    print(f"Diff: {z - z_expected:46b}")

    solution_part_2 = 0
    print(solution_part_2)


def calculate_decimal(var_name: Literal["x", "y", "z"], known_wires: dict[str, bool]) -> int:
    relevant_wires = filter(lambda x: x[0].startswith(var_name), known_wires.items())
    decimal = 0
    for wire, value in relevant_wires:
        shift = int(wire[1:])  # Extract bit index (0 = LSB) from name
        decimal += int(value) << shift  # Convert Bool to 0 or 1, bitshift to appropriate position/power of 2
    return decimal


class CircuitVisualizer(QGraphicsScene):
    def __init__(self, gates, parent=None):
        super().__init__(parent)
        self.gates = gates
        self.gate_positions = {}  # Store the center positions of gate outputs
        self.input_positions = {}  # Store positions for gate inputs

    def draw_circuit(self):
        y = 0  # Vertical spacing for gates
        x_spacing = 150  # Horizontal spacing between gates
        self.setBackgroundBrush(Qt.white)

        # Draw gates and store positions
        for (output_label, gate_label), inputs in self.gates.items():
            x = len(self.gate_positions) * x_spacing

            # Draw the gate as a rectangle
            gate_item = QGraphicsRectItem(x, y, 100, 50)
            gate_item.setBrush(Qt.lightGray)
            self.addItem(gate_item)

            # Add label to the gate
            label_item = QGraphicsTextItem(f"{gate_label}\n[{output_label}]")
            label_item.setParentItem(gate_item)
            label_item.setPos( x + 10,  y + 10)

            # Store the position of the gate's output
            gate_center = QPointF(x + 100, y + 25)
            self.gate_positions[output_label] = gate_center

            # Store the positions for inputs
            for gate_type, input_label in inputs:
                input_pos = QPointF(x, y + (inputs.index((gate_type, input_label)) * 25))
                self.input_positions.setdefault(input_label, []).append(input_pos)

            y += 100  # Adjust vertical spacing for the next gate

        # Draw connections between gates
        self.draw_connections()

    def draw_connections(self):
        pen = QPen(Qt.black)
        pen.setWidth(2)

        for (output_label, gate_label), inputs in self.gates.items():
            output_pos = self.gate_positions[output_label]
            for gate_type, input_label in inputs:
                if input_label in self.gate_positions:  # If the input is from another gate's output
                    input_pos = self.gate_positions[input_label]
                elif input_label in self.input_positions:  # If the input is an initial input
                    input_pos = self.input_positions[input_label][0]  # Take the first position for simplicity
                else:
                    continue

                # Draw the connection line
                self.addLine(input_pos.x(), input_pos.y(), output_pos.x(), output_pos.y(), pen)


def main():
    app = QApplication([])

    # Example circuit
    gates = {
        ("out1", "g1"): [(Gate.AND, "in1"), (Gate.OR, "in2")],
        ("out2", "g2"): [(Gate.XOR, "out1"), (Gate.AND, "in3")],
        ("out2", "in1"): [(Gate.AND, "out3")],
    }

    # Visualize circuit
    scene = CircuitVisualizer(gates)
    scene.draw_circuit()

    view = QGraphicsView(scene)
    view.setWindowTitle("Circuit Visualizer")
    view.show()

    app.exec_()


if __name__ == "__main__":
    solve(Path("input.txt"))
    main()