import xml.etree.ElementTree as ET
from adb_control.core.base import ADBBase


class UIExtractor(ADBBase):
    def __init__(
        self, adb_path="adb", attributes=["resource-id", "text", "class", "package"]
    ):
        super().__init__(adb_path)
        self.attributes = attributes

    def uiautomator(self) -> dict:
        """
        Extract and process UI data from the device in real-time.
        """
        try:
            dump_path = "/sdcard/window_dump.xml"
            self.shell_command(f"uiautomator dump {dump_path}")

            local_file = "window_dump.xml"
            self.transfer_file(
                direction="pull", remote_file_path=dump_path, local_file_path=local_file
            )

            self.remove_file(dump_path)

            ui_data = self._parse_ui_hierarchy(local_file)

            return {
                "status": "success",
                "data": ui_data,
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to extract UI: {str(e)}",
            }

    def _parse_ui_hierarchy(self, file_path: str) -> dict:
        """
        Parse the UI hierarchy XML file and extract relevant data.

        :param file_path: Path to the XML file.
        :return: Parsed data as a dictionary.
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            ui_elements = []
            for node in root.iter("node"):
                element = {attr: node.attrib.get(attr, "") for attr in self.attributes}
                ui_elements.append(element)
            return {"elements": ui_elements}

        except Exception as e:
            raise Exception(f"Error parsing UI hierarchy XML: {e}")

    def find_element(self, element_id: str) -> dict:
        """
        Find an element by resource-id or text.

        :param element_id: The resource-id or text to filter by.
        :return: The matched element or an error message.
        """
        try:
            ui_data = self.uiautomator()
            if ui_data["status"] == "error":
                return ui_data

            element = self._get_element_by_id(ui_data["data"]["elements"], element_id)
            if element["element"] == "not found":
                return {
                    "status": "error",
                    "message": "Element not found.",
                }

            return {
                "status": "success",
                "element": element["element"],
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to find element: {str(e)}",
            }

    def _get_element_by_id(self, ui_elements: list, element_id: str) -> dict:
        """
        Find an element by resource-id or text.

        :param ui_elements: List of parsed UI elements.
        :param element_id: The resource-id or text to filter by.
        :return: The matched element or an empty dictionary if not found.
        """
        for element in ui_elements:
            if element["resource_id"] == element_id or element["text"] == element_id:
                return {"element": element}
        return {"element": "not found"}
