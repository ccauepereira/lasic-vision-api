import { Image } from 'lucide-react';

export function EstadoVazio() {
  return (
    <div className="estado-vazio">
      <Image size={48} color="#ccc" />
      <h2>Nenhuma tarefa selecionada</h2>
      <p>Selecione uma tarefa na lista lateral ou crie uma nova.</p>
    </div>
  );
}