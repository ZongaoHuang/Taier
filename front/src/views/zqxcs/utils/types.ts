interface FormItemProps {
  id?: number;
  name: string;
  data: any;
  scale: string;
}
interface FormProps {
  formInline: FormItemProps;
}

export type { FormItemProps, FormProps};
