from typing import Any, Dict, List, Optional

import rclpy
from rclpy.node import Node
from rcl_interfaces.srv import ListParameters, GetParameters, SetParameters
from rcl_interfaces.msg import Parameter, ParameterType, ParameterValue

class RemoteParamFetcher:
    def __init__(self, node: Node, remote_node_name: str) -> None:
        self._node = node
        self._remote = remote_node_name if remote_node_name.startswith('/') else f'/{remote_node_name}'
        self._list_cli = node.create_client(ListParameters, f'{self._remote}/list_parameters')
        self._get_cli = node.create_client(GetParameters, f'{self._remote}/get_parameters')
        self._set_cli = node.create_client(SetParameters, f'{self._remote}/set_parameters')
    def fetch_all(self, timeout_sec: float = 1.0) -> Dict[str, Any]:
        # wait for services
        if not self._list_cli.wait_for_service(timeout_sec=timeout_sec):
            raise RuntimeError(f'No service: {self._remote}/list_parameters')
        if not self._get_cli.wait_for_service(timeout_sec=timeout_sec):
            raise RuntimeError(f'No service: {self._remote}/get_parameters')

        # 1) list parameter names
        list_req = ListParameters.Request()
        list_req.prefixes = []
        list_req.depth = 0  # recursive
        list_fut = self._list_cli.call_async(list_req)
        rclpy.spin_until_future_complete(self._node, list_fut, timeout_sec=timeout_sec)
        list_resp = list_fut.result()
        if list_resp is None:
            raise RuntimeError(f'list_parameters failed: {list_fut.exception()}')
            
        names = list_resp.result.names

        # 2) get parameter values
        get_req = GetParameters.Request()
        get_req.names = names
        get_fut = self._get_cli.call_async(get_req)
        rclpy.spin_until_future_complete(self._node, get_fut, timeout_sec=timeout_sec)
        get_resp = get_fut.result()
        if get_resp is None:
            raise RuntimeError(f'get_parameters failed: {get_fut.exception()}')


        # 3) build dict
        out: Dict[str, Any] = {}
        for name, pv in zip(names, get_resp.values):
            out[name] = _pv_to_py(pv)
        return out

    def set_all(self, params: Dict[str, Any], timeout_sec: float = 1.0) -> List[bool]:
        """Set parameters on the remote node.
        
        Args:
            params: Dict of parameter names to values
            timeout_sec: Timeout for service calls
            
        Returns:
            List of success bools for each parameter
        """
        if not self._set_cli.wait_for_service(timeout_sec=timeout_sec):
            raise RuntimeError(f'No service: {self._remote}/set_parameters')

        # Build parameter list
        param_list = []
        for name, value in params.items():
            param = Parameter()
            param.name = name
            param.value = _py_to_pv(value)
            param_list.append(param)

        # Call set_parameters
        set_req = SetParameters.Request()
        set_req.parameters = param_list
        set_fut = self._set_cli.call_async(set_req)
        rclpy.spin_until_future_complete(self._node, set_fut, timeout_sec=timeout_sec)
        set_resp = set_fut.result()
        if set_resp is None:
            raise RuntimeError(f'set_parameters failed: {set_fut.exception()}')

        return [r.successful for r in set_resp.results]


def _py_to_pv(value: Any) -> ParameterValue:
    """Convert a Python value to a ParameterValue message."""
    pv = ParameterValue()
    if value is None:
        pv.type = ParameterType.PARAMETER_NOT_SET
    elif isinstance(value, bool):
        pv.type = ParameterType.PARAMETER_BOOL
        pv.bool_value = value
    elif isinstance(value, int):
        pv.type = ParameterType.PARAMETER_INTEGER
        pv.integer_value = value
    elif isinstance(value, float):
        pv.type = ParameterType.PARAMETER_DOUBLE
        pv.double_value = value
    elif isinstance(value, str):
        pv.type = ParameterType.PARAMETER_STRING
        pv.string_value = value
    elif isinstance(value, (list, tuple)):
        if len(value) == 0:
            pv.type = ParameterType.PARAMETER_NOT_SET
        elif isinstance(value[0], bool):
            pv.type = ParameterType.PARAMETER_BOOL_ARRAY
            pv.bool_array_value = list(value)
        elif isinstance(value[0], int):
            pv.type = ParameterType.PARAMETER_INTEGER_ARRAY
            pv.integer_array_value = list(value)
        elif isinstance(value[0], float):
            pv.type = ParameterType.PARAMETER_DOUBLE_ARRAY
            pv.double_array_value = list(value)
        elif isinstance(value[0], str):
            pv.type = ParameterType.PARAMETER_STRING_ARRAY
            pv.string_array_value = list(value)
    return pv


def _pv_to_py(pv) -> Any:
    t = pv.type
    if t == ParameterType.PARAMETER_NOT_SET:
        return None
    if t == ParameterType.PARAMETER_BOOL:
        return pv.bool_value
    if t == ParameterType.PARAMETER_INTEGER:
        return pv.integer_value
    if t == ParameterType.PARAMETER_DOUBLE:
        return pv.double_value
    if t == ParameterType.PARAMETER_STRING:
        return pv.string_value
    if t == ParameterType.PARAMETER_BYTE_ARRAY:
        return list(pv.byte_array_value)
    if t == ParameterType.PARAMETER_BOOL_ARRAY:
        return list(pv.bool_array_value)
    if t == ParameterType.PARAMETER_INTEGER_ARRAY:
        return list(pv.integer_array_value)
    if t == ParameterType.PARAMETER_DOUBLE_ARRAY:
        return list(pv.double_array_value)
    if t == ParameterType.PARAMETER_STRING_ARRAY:
        return list(pv.string_array_value)
    return None

