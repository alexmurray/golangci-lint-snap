import snapcraft

from snapcraft.plugins.v1 import dump


class FetchGolangCILint(snapcraft.BasePlugin):
    @classmethod
    def schema(cls):
        schema = super().schema()

        schema['properties']['version'] = {
            'type': 'string',
        }
        schema['required'] = ['version']
        return schema

    def golangci_lint_arch(self):
        arch = self.project.deb_arch
        if arch == 'i386':
            arch = '386'
        elif arch == 'armhf':
            arch = 'armv7'
        return arch

    def pull(self):
        super().pull()
        snapcraft.sources.Tar(
            'https://github.com/golangci/golangci-lint/releases/download/'
            'v{version}/golangci-lint-{version}-linux-{arch}.tar.gz'
            .format(arch=self.golangci_lint_arch(),
                    version=self.options.version),
            self.sourcedir).pull()

    def build(self):
        super().build()
        snapcraft.file_utils.link_or_copy_tree(
            self.builddir, self.installdir,
            copy_function=lambda src, dst: dump._link_or_copy(src, dst, self.installdir))
