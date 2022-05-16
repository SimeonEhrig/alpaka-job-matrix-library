"""Used software in the CI tests."""

from typing import Dict, List, Tuple
from typeguard import typechecked

from alpaka_job_coverage.globals import *  # pylint: disable=wildcard-import,unused-wildcard-import
from example_globals import *  # pylint: disable=wildcard-import,unused-wildcard-import


sw_versions: Dict[str, List[str]] = {
    GCC: ["5", "6", "7", "8", "9", "10", "11"],
    CLANG: ["6.0", "7", "8", "9", "10", "11", "12", "13", "14", "15"],
    NVCC: ["10.0", "11.0", "11.1", "11.2", "11.3", "11.4", "11.5", "11.6"],
    HIPCC: ["4.3", "4.5", "5.0", "5.1"],
    BACKENDS: [
        ALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLE,
        ALPAKA_ACC_CPU_B_OMP2_T_SEQ_ENABLE,
        ALPAKA_ACC_GPU_CUDA_ENABLE,
        ALPAKA_ACC_GPU_HIP_ENABLE,
    ],
    UBUNTU: ["18.04", "20.04"],  # not used yet
    CMAKE: ["3.18.6", "3.19.8", "3.20.6", "3.21.6", "3.22.3"],
    BOOST: [
        "1.66.0",
        "1.67.0",
        "1.74.0",
        "1.75.0",
        "1.76.0",
        "1.77.0",
        "1.78.0",
    ],
    ALPAKA: ["0.6.0", "0.6.1", "0.7.0", "0.8.0", "0.9.0", "develop"],
    CXX_STANDARD: ["14", "17", "20"],
}


@typechecked
def get_compiler_versions(clang_cuda: bool = True) -> List[Tuple[str, str]]:
    """Generate a list of compiler name version tuple.

    Args:
        clang_cuda (bool, optional): If true, create entries for cling-cuda basing on the clang
        version. Defaults to True.

    Returns:
        List[Tuple[str, str]]: The compiler name version tuple list.
    """
    compilers: List[Tuple[str, str]] = []

    for compiler_name in [GCC, CLANG, NVCC, HIPCC]:
        for version in sw_versions[compiler_name]:
            compilers.append((compiler_name, version))
            if clang_cuda and compiler_name == CLANG:
                compilers.append((CLANG_CUDA, version))

    return compilers


@typechecked
def get_backend_versions() -> List[List[Tuple[str, str]]]:
    """Generate a list of all backend state combinations for each alpaka backend. There are two
    cases:

    1. The backend has only the states `on` and `off`
    2. The backend has version numbers: `off`, `1.0`, `2.0` ...

    Each inner list contains all states for a single backend. The outer list contains all state list
    of each backend.

    Returns:
        List[List[Tuple[str, str]]]: List with the alpaka backend states.
    """
    backends: List[List[Tuple[str, str]]] = []

    for backend_name in sw_versions[BACKENDS]:
        backend_list = [(backend_name, OFF)]
        if backend_name == ALPAKA_ACC_GPU_CUDA_ENABLE:
            for version in sw_versions[NVCC]:
                backend_list.append((backend_name, version))
        elif backend_name == ALPAKA_ACC_GPU_HIP_ENABLE:
            for version in sw_versions[HIPCC]:
                backend_list.append((backend_name, version))
        else:
            backend_list.append((backend_name, ON))
        backends.append(backend_list)

    return backends


@typechecked
def get_backend_combination_matrix() -> List[List[Tuple[str, str]]]:
    """Generates a NxN combination matrix of all available alpaka backends.

    Returns:
        List[List[Tuple[str, str]]]: NxN combination matrix of all alpaka backends.
    """
    combination_matrix: List[List[Tuple[str, str]]] = []

    create_combination_matrix(0, [], get_backend_versions(), combination_matrix)

    return combination_matrix


@typechecked
def create_combination_matrix(
    index: int,
    current_combination: List[Tuple[str, str]],
    input_list: List[List[Tuple[str, str]]],
    combination_matrix: List[List[Tuple[str, str]]],
):
    """Recursive function to generate the NxN combination matrix.

    Args:
        index (int): Index of the current alpaka backend.
        current_combination (List[Tuple[str, str]]): Current combination (can be incomplete).
        input_list (List[List[Tuple[str, str]]]): List of available alpaka backends.
        combination_matrix (List[List[Tuple[str, str]]]): Output combination matrix.
    """
    if index < len(input_list):
        for version in input_list[index]:
            current_combination_copy = current_combination[:]
            current_combination_copy.append(version)
            create_combination_matrix(
                index + 1, current_combination_copy, input_list, combination_matrix
            )
    else:
        combination_matrix.append(current_combination)


@typechecked
def get_backend_single_matrix() -> List[List[Tuple[str, str]]]:
    """Generate backend list, where only backend is active on the same time.

    Returns:
        List[List[Tuple[str, str]]]: The backend list.
    """
    combination_matrix: List[List[Tuple[str, str]]] = []
    combination_matrix.append(
        [
            (ALPAKA_ACC_CPU_B_SEQ_T_SEQ_ENABLE, ON),
            (ALPAKA_ACC_CPU_B_OMP2_T_SEQ_ENABLE, ON),
        ]
    )

    for cuda_version in sw_versions[NVCC]:
        combination_matrix.append([(ALPAKA_ACC_GPU_CUDA_ENABLE, cuda_version)])

    for rocm_version in sw_versions[HIPCC]:
        combination_matrix.append([(ALPAKA_ACC_GPU_HIP_ENABLE, rocm_version)])

    return combination_matrix


@typechecked
def get_sw_tuple_list(name: str) -> List[Tuple[str, str]]:
    """Creates a list of software name version tuples for a software name.

    Args:
        name (str): Name of the software

    Returns:
        List[Tuple[str, str]]: List of software name versions tuples.
    """
    tuple_list: List[Tuple[str, str]] = []
    for version in sw_versions[name]:
        tuple_list.append((name, version))

    return tuple_list
