interface FormItemProps {
  id?: string;
  name: string;
  suite_name: string;
  file?: File;
  created_at?: string;
  question_count?: number;
  cate?: string;
}
interface FormProps {
  formInline: FormItemProps;
}

export type { FormItemProps, FormProps};
