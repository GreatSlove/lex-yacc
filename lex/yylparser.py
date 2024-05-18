class YylParser:
    def __init__(self, filename):
        self.program1 = ""
        self.define_rules = {}
        self.regex_rules = []
        self.program2 = ""
        self.init_all(filename)

    def ln_to_pair(self, ln):
        left, right = ln.split(maxsplit=1)
        return left, right

    def read_from_stream(self, ifile):
        step = 0
        in_def = False

        for ln in ifile:
            ln = ln.strip()

            if in_def:
                if ln == "%}":
                    in_def = False
                else:
                    self.program1 += ln + "\n"
                continue

            if ln == "%{":
                in_def = True
                continue

            if ln == "%%":
                step += 1
                continue

            if ln == "":
                continue

            if step == 0:
                left, right = self.ln_to_pair(ln)
                self.define_rules[left] = right
            elif step == 1:
                left, right = self.ln_to_pair(ln)
                self.regex_rules.append((left, right))
            elif step == 2:
                self.program2 += ln
            else:
                raise Exception("Unexpected parsing step")

    def init_all(self, filename):
        with open(filename, "r") as ifile:
            self.read_from_stream(ifile)

 