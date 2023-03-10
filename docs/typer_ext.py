import re
from typing import Any, Dict, Generator, List, Tuple, Union

import click
import sphinx_click.ext as sphinx_click
import typer
from docutils import statemachine
from sphinx import application


def _get_help_record(
    parameter: Union[click.Option, click.Argument]
) -> Tuple[str, str]:
    def _write_option_opts(opts: List[str]) -> str:
        rv, _ = click.formatting.join_options(opts)
        if not parameter.is_flag and not parameter.count:
            name = parameter.name
            if parameter.metavar:
                name = parameter.metavar.lstrip('<[{($').rstrip('>]})$')
            rv += ' <{}>'.format(name)
        return rv

    if isinstance(parameter, click.Option):
        rv = [_write_option_opts(parameter.opts)]
        if parameter.secondary_opts:
            rv.append(_write_option_opts(parameter.secondary_opts))
    else:
        rv = [parameter.name.upper()]

    out = []
    if getattr(parameter, 'help', None):
        help_lines = parameter.help.replace('\b', '\b\b').split('\b')
        out.extend(help_lines)

    extras = []
    if getattr(parameter, 'show_default', None):
        parameter_default = '[default: {}]'
        if isinstance(parameter.show_default, str):
            extras.append(parameter_default.format(parameter.show_default))
        elif parameter.default:
            extras.append(parameter_default.format(parameter.default))

    metavar = parameter.make_metavar()
    if isinstance(parameter, click.Argument) and re.match(
        rf'\[?{parameter.name.upper()}]?', metavar
    ):
        metavar = parameter.type.name.upper()

    if metavar != 'BOOLEAN' or isinstance(parameter, click.Argument):
        extras.append(f'*({metavar})*')

    if parameter.required:
        extras.append('*[required]*')

    if extras:
        if out:
            out.append('')

        out.extend(extras)

    return ', '.join(rv), '\n'.join(out)


def _format_parameter(
    parameter: Union[click.Option, click.Argument]
) -> Generator[str, None, None]:
    parameter_help = _get_help_record(parameter)
    yield '.. option:: {}'.format(parameter_help[0])
    if parameter_help[1]:
        yield ''
        bar_enabled = False
        for line in statemachine.string2lines(
            sphinx_click.ANSI_ESC_SEQ_RE.sub('', parameter_help[1]),
            tab_width=4,
            convert_whitespace=True,
        ):
            if line == '\b':
                bar_enabled = True
                continue
            if line == '':
                bar_enabled = False
            line = '| ' + line if bar_enabled else line
            yield sphinx_click._indent(line)


sphinx_click._format_option = _format_parameter
sphinx_click._format_argument = _format_parameter


class TyperDirective(sphinx_click.ClickDirective):
    def _load_module(
        self, module_path: str
    ) -> Union[click.Command, click.Group]:
        module_name, attr_name = module_path.split(':', 1)
        mod = __import__(module_name, globals(), locals(), [attr_name])
        typer_instance = getattr(mod, attr_name)
        parser = typer.main.get_command(typer_instance)
        return parser


def setup(app: application.Sphinx) -> Dict[str, Any]:
    app.add_directive('typer', TyperDirective)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
