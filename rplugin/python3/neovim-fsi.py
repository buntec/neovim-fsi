import threading
from subprocess import Popen, PIPE
from queue import Queue

import uuid
import pynvim


@pynvim.plugin
class NeovimFsi(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.fsi = None
        self.count = 0

    def notify(self, msg):
        self.nvim.out_write('neovim-fsi[info]> {}\n'.format(msg))

    def error(self, msg):
        self.nvim.out_write('neovim-fsi[error]> {}\n'.format(msg))

    def _read_stdout(self):
        for line in self.fsi.stdout:
            self.queue.put(line, block=True)

    def _read_stderr(self):
        for line in self.fsi.stderr:
            self.queue.put(line, block=True)

    def _write_buffer(self):
        while True:
            try:
                output = self.queue.get(True, 0.5)
                lines = output.split('\n')
                self.nvim.async_call(self.write_to_output_buffer, lines)
            except:
                pass

    def write_to_output_buffer(self, lines):
        buf_nr = self.nvim.call('bufnr', 'fsi-output')
        if buf_nr != -1:
            buf = self.nvim.buffers[buf_nr]
            buf.append(lines)
            winids = self.nvim.call('win_findbuf', buf_nr)
            if winids:
                self.nvim.call('win_gotoid', winids[0])
                self.nvim.command('normal! G')
                self.nvim.command('wincmd p')
                self.notify(self.count)
                self.count += 1

    @pynvim.command('FsiCreateBuffer')
    def create_fsi_buffer(self):
        self.nvim.command('badd fsi-output')
        self.nvim.command('botright 12 new')
        self.nvim.command('edit {}'.format('fsi-output'))
        self.nvim.command('setlocal bufhidden=wipe')
        self.nvim.command('setlocal nobuflisted')
        self.nvim.command('setlocal buftype=nowrite')
        self.nvim.command('setlocal noswapfile')
        self.nvim.command('setlocal nospell')
        self.nvim.command('wincmd p')
        # self.nvim.request('nvim_buf_set_option', fsi_buf, 'buftype', 'nowrite')
        # self.nvim.request('nvim_buf_set_option', fsi_buf, 'bufhidden', 'hide')
        # self.nvim.request('nvim_buf_set_option', fsi_buf, 'swapfile', False)

    @pynvim.command('FsiStart')
    def start_fsi(self):
        fsi_server_id = 'vim-' + str(uuid.uuid4())
        command = ['fsharpi', '--fsi-server:{}'.format(fsi_server_id), '--nologo']
        output_file = open('fsi-output', 'w')
        opts = {'stdin': PIPE,
                'stdout': output_file,
                'stderr': output_file,
                'shell': False,
                'universal_newlines': True}
        self.fsi = Popen(command, **opts)
        self.queue = Queue()
        # self.t1 = threading.Thread(target=self._read_stdout, daemon=True)
        # self.t2 = threading.Thread(target=self._read_stderr, daemon=True)
        # self.t3 = threading.Thread(target=self._write_buffer, daemon=True)
        # self.t1.start()
        # self.t2.start()
        # self.t3.start()

    @pynvim.command('FsiShow')
    def show_fsi(self):
        self.nvim.command('sb fsi-output')

    @pynvim.command('FsiStop')
    def kill_fsi(self):
        if self.fsi is not None:
            self.fsi.kill()

    def send_to_fsi(self, code):
        self.fsi.stdin.write('{}\n'.format(code))
        self.fsi.stdin.write(';;\n')
        self.fsi.stdin.flush()

    @pynvim.command('FsiSendBuffer')
    def send_buffer_to_fsi(self):
        buf = self.nvim.current.buffer
        content = '\n'.join(buf)
        self.send_to_fsi(content)

    @pynvim.command('FsiRead')
    def read_from_fsi(self):
        # lines = []
        for line in self.fsi.stdout:
            self.notify(line)
        # fsi_output = '\n'.join(lines)
        self.nvim.command('let fsioutput = "{}"'.format("blahblah"))
        self.nvim.command('botright 12 new')
        self.nvim.command('edit {}'.format('fsi-output'))
        self.nvim.command('setlocal bufhidden=wipe')
        self.nvim.command('setlocal nobuflisted')
        self.nvim.command('setlocal buftype=nofile')
        self.nvim.command('setlocal noswapfile')
        self.nvim.command('setlocal nospell')
        self.nvim.command('0 put =fsioutput')

    @pynvim.command('FsiTest')
    def fsi_test(self):
        self.notify('this is a test')
