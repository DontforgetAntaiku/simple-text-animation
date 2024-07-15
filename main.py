import itertools
import os
import re
import time

pattern = re.compile(r"[#\n\r\t*&.,_↓←]")

input_string = input().strip()
output_string = input().strip()
max_len = 17
fps = 5
delay = 1 / fps
for i in [input_string, output_string]:
    if re.search(pattern, i):
        print(r"Technical symbols have been found! Do not use them (#\n\r\t*&.,_↓←)")
        exit()
    elif len(i) > max_len:
        print("String length exceeds maximum(>17)")
        exit()
output_string_tmp = output_string
current_output = "*" * len(output_string)
base_lines = {
    0: lambda x: x.rjust(max_len, "."),
    1: "→→→→→→↓←←←←←←←←←←",
    2: "Check:_→→→→→→→→→↓",
    3: "......→→→→↓.....↓",
    4: "Transform:_→→→→→↓",
    5: "↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓",
}
line2 = list(base_lines[1])
line3 = list(base_lines[2])
line4 = list(base_lines[3])
line5 = list(base_lines[4])
line6 = list(base_lines[5])
stop = False
generate_stage = 0


def get_current_frame():
    global \
        input_string, \
        output_string, \
        base_lines, \
        current_output, \
        stop, \
        line2, \
        line3, \
        line4, \
        line5, \
        line6, \
        output_string_tmp, \
        generate_stage
    current_frame = []
    # first row
    line1 = base_lines[0](input_string)
    current_frame.append(line1)

    # third row
    current_frame.append("".join(line2))
    current_frame.append("".join(line3))
    current_frame.append("".join(line4))
    current_frame.append("".join(line5))
    current_frame.append("".join(line6))

    # last row and line6

    current_frame.append(current_output.rjust(max_len, "."))
    if len(output_string_tmp) == 0 and stop and line6[0] != "↓":
        stop = False
    for i, letter in enumerate(line6):
        if letter == output_string.rjust(max_len, ".")[i]:
            index = output_string.rindex(letter)
            output_string = list(output_string)
            output_string[index] = "#"
            output_string = "".join(output_string)
            output_string_tmp = "".join(output_string.replace("#", ""))
            tmp = list(current_output)
            tmp[index] = letter
            current_output = "".join(tmp)
            line6[i] = "↓"
            stop = False
            break

    line6 = line6[1:]
    line6.append("↓")

    # line5
    if line5[-1] != "↓":
        line6[-1] = line5[-1]
        line5[-1] = "↓"
    if line5[-2] != "→":
        line5[-1] = line5[-2]
        line5[-2] = "→"
    line5.insert(-6, "→")
    line5.pop(-2)
    if generate_stage == 8:
        line5[-6] = output_string_tmp[0]
        line5[-7] = "_"
        generate_stage = 0
        stop = True
    elif not stop and "*" in current_output and not len(input_string):
        line5[-7] = next(loading_chars)
        generate_stage += 1
    if line5[-7] != "_" and generate_stage == 0:
        for i in range(len(output_string_tmp)):
            if output_string_tmp[i] not in input_string or input_string.count(
                output_string_tmp[i]
            ) < output_string.count(output_string_tmp[i]):
                line5[-6] = output_string_tmp[i]
                break
        line5[-7] = "_"
    # line4
    if line4[-1] != "↓":
        line5[-1] = line4[-1]
        line4[-1] = "↓"

    if line4[-7] != "↓":
        line5[-7] = line4[-7]
        line4[-7] = "↓"
    if line4[-8] != "→":
        line4[-7], line4[-8] = line4[-8], ""
    line4.insert(-11, "→")
    line4.pop(-8)
    # line3
    if line3[-1] != "↓":
        line4[-1], line3[-1] = line3[-1], "↓"

    if line3[-2] != "→":
        line3[-1] = line3[-2]
        line3[-2] = "→"

    line3.insert(-10, "→")
    del line3[-2]
    if line3[-11] != "_":
        if len(output_string_tmp) == 0:
            line3[-10] = "?"
            line3[-11] = "_"
        elif line3[-11] in output_string_tmp:
            line3[-10] = line3[-11]
            line3[-11] = "_"
            output_string_tmp = (
                output_string_tmp[: output_string_tmp.find(line3[-10])]
                + output_string_tmp[output_string_tmp.find(line3[-10]) + 1 :]
            )
        else:
            line4[-11] = line3[-11]
            line3[-11] = "_"
            # output_string_tmp = output_string_tmp[1:]

    # line2
    if line2[6] != "↓":
        line3[6] = line2[6]
        line2[6] = "↓"

    if line2[5] != "→":
        line2[6] = line2[5]
        line2[5] = "→"

    line2.insert(0, "→")
    del line2[5]

    if line2[7] != "←":
        line2[6] = line2[7]
        line2[7] = "←"
    line2.append("←")
    line2.pop(7)

    if not stop:
        letter = "&"
        if len(input_string):
            letter = input_string[0]
            tmp = input_string.rjust(max_len, ".")
            index = tmp.index(letter)
            input_string = input_string[1:]
            stop = True
        if letter != "&":
            line2[index] = letter
    return current_frame


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


clear_console()

loading_chars = itertools.cycle(["\\", "|", "/", "-"])
for i in range(15):
    char = next(loading_chars)
    print(f"\rLoading {char}", end="", flush=True)
    time.sleep(0.1)


while "*" in current_output or stop:
    clear_console()
    text = get_current_frame()
    # for i in text:
    #     print(f'\r{i}\n', end='', flush=True)
    print("\n".join(text))
    time.sleep(delay)
clear_console()
print(current_output)
