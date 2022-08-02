import { spider_provider } from "../providers/spider_provider";

export const spider_repository = {
  get_aws_data: async () => {
    const response = await spider_provider.get_aws_data();
    return response;
  },
};
