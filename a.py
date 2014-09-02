
def is_digital(s):
    if s >= "0" and s <= "9":
        return True
    return False

"""
lines = open("1.txt").readlines()

s = ""
for line in lines:
    line = line.strip()
    if line:
        if is_digital(line[0]) or is_digital(line[1]):
            line = "|||" + line
        line = line.replace("a", "A").replace("b", "B").replace("c", "C").replace("d", "D")
        s += line + "\n"

open("01.txt", "w").write(s)
"""


lines = open("4.txt").readlines()

s = ""
for line in lines:
    line = line.strip()
    if line:
        if is_digital(line[0]) or is_digital(line[1]):
            line = "|||" + line
        line = line.replace("a", "A").replace("b", "B").replace("c", "C").replace("d", "D")
        s += line + "\n"

open("04.txt", "w").write(s)




print "ok"
