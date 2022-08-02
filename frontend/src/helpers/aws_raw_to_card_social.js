const example_data = [
  {
    title: "Nuevos Puntos de Venta",
    icon: "person",
    value: "321",
    color1: "#7cb342",
    color2: "#3e51b5",
  },
];

export const structure_aws_data_card = (aws_data, icon, color1, color2) => {
  const { value, unit, label } = aws_data;

  return {
    title: `${label} ${unit}`,
    icon: `${icon}`,
    value: value === null ? "No hay datos" : `${value}`,
    color1: `${color1}`,
    color2: `${color2}`,
  };
};
