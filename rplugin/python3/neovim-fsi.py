import pynvim


@pynvim.plugin
class NeovimFsi(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.channel = None

    def notify(self, msg):
        self.nvim.out_write("neovim-fsi> {}\n".format(msg))

    def send_lines_to_fsi(self, lines):
        try:
            self.nvim.call("chansend", self.channel, lines)
        except Exception:
            pass

    @pynvim.command("FsiOpen")
    def fsi_open(self):
        if self.nvim.call("exists", "g:neovim_fsi_window_height"):
            height = self.nvim.eval("g:neovim_fsi_window_height")
        else:
            height = 12  # defaul fsi window height
        if self.nvim.call("exists", "g:neovim_fsi_command"):
            fsi_command = self.nvim.eval("g:neovim_fsi_command")
        else:
            fsi_command = "dotnet fsi"  # defaults to dotnet core cli
        self.nvim.command("botright {} new".format(height))
        self.nvim.command("terminal {}".format(fsi_command))
        self.channel = self.nvim.eval("&channel")
        self.nvim.command("normal! G")
        self.nvim.command("wincmd p")

    @pynvim.command("FsiSendBuffer")
    def send_buffer_to_fsi(self):
        buf = self.nvim.current.buffer
        lines = list(buf)
        lines.extend([";;", "\n"])
        self.send_lines_to_fsi(lines)

    @pynvim.command("FsiSendLine")
    def send_line_to_fsi(self):
        line = self.nvim.call("getline", ".")
        lines = [line, ";;", "\n"]
        self.send_lines_to_fsi(lines)

    @pynvim.command("FsiSendSelection")
    def send_selection_to_fsi(self):
        buf = self.nvim.current.buffer
        (lnum1, col1) = buf.mark("<")
        (lnum2, col2) = buf.mark(">")
        lines = self.nvim.eval("getline({}, {})".format(lnum1, lnum2))
        # lines[0] = lines[0][col1:]
        # lines[-1] = lines[-1][:col2]
        lines.extend([";;", "\n"])
        self.send_lines_to_fsi(lines)
