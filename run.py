import sys
from pathlib import Path
from os.path import abspath, join, dirname

REPO_ROOT = dirname(abspath(__file__))
PATH_TO_TSFPGA = join(REPO_ROOT, "tsfpga")
PATH_TO_VUNIT = join(REPO_ROOT, "vunit")
sys.path.insert(0, str(PATH_TO_TSFPGA))
sys.path.insert(0, str(PATH_TO_VUNIT))


import tsfpga

from tsfpga.module import get_hdl_modules, get_modules
from tsfpga.examples.simulation_utils import (
    SimulationProject,
    get_arguments_cli,
    create_vhdl_ls_configuration,
)


def main():

    cli = get_arguments_cli(default_output_path=Path(REPO_ROOT))
    args = cli.parse_args()

    modules = get_hdl_modules()  # Add TSFPGA modules
    # modules = get_modules()  # Add project modules

    simulation_project = SimulationProject(args=args)

    simulation_project.add_modules(args=args, modules=modules)
    ip_core_vivado_project_directory = (
        simulation_project.add_vivado_simlib_and_ip_cores(args=args, modules=modules)
    )

    create_vhdl_ls_configuration(
        output_path=Path(REPO_ROOT),
        temp_files_path=Path(REPO_ROOT),
        modules=modules,
        ip_core_vivado_project_directory=ip_core_vivado_project_directory,
    )

    simulation_project.vunit_proj.main()


if __name__ == "__main__":
    main()
