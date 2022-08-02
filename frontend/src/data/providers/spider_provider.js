import { axiosClient } from "src/boot/axios";
import { base_URL } from "src/config";


export const spider_provider = {
  get_aws_data: async () => {
    try {
      const response = await axiosClient(base_URL).get("/metrics/all");
      console.log(response)
      return fromAxiosResponse(response);
    } catch (error) {
      return axiosError(error);
    }
  }
}


const fromAxiosResponse = (response) => {
  if (response.headers["content-type"] != "application/json") {
    return {
      "success": false,
      "error": {
        "code": "not_json",
        "text": "La respuesta no es un JSON",
      }
    };
  } else if (!isAxiosResponse(response)) {
    return {
      "success": false,
      "error": {
        "code": "not_aca",
        "text": "La respuesta no es Acapuedo",
      }
    };
  } else if (response.status >= 200 && response.status < 300 && response.data["meta"]["status"] == "success") {
    return {
      "success": true,
      "data": response.data.data,
    };
  } else {
    return extractAxiosError(response);
  }
}


const axiosError = (e) => {
  if (!e.response) {
    return {
      "success": false,
      "error": {
        "code": "unexpected",
        "text": "No se pudo conectar con el servidor, asegurese de tener acceso a internet.",
      }
    }
  } else {
    return extractAxiosError(e);
  }
}

const isAxiosResponse = (response) => {
  if (response.data instanceof Object && response.data.hasOwnProperty("meta")) {
    return true
  } else {
    return false
  }
}

const extractAxiosError = (e) => {
  const { response } = e;
  const { meta } = response;
  return {
    "success": false,
    "error": {
      "code": meta.code,
      "text": meta.description,
    }
  }
}