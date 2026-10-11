import java.sql.*;
/** Fixture local de AP9. No reemplaza un endpoint de anulación del sistema. */
class PrepararVentaAnulada {
  public static void main(String[] args) throws Exception {
    long id=Long.parseLong(args[0]);
    try(Connection c=DriverManager.getConnection(System.getenv("DB_URL"),System.getenv("DB_USERNAME"),System.getenv("DB_PASSWORD"))){
      c.setAutoCommit(false);
      try {
        try(PreparedStatement p=c.prepareStatement("select v.estado, cl.nombres from ventas v join clientes cl on cl.id=v.cliente_id where v.id=? for update")){
          p.setLong(1,id);try(ResultSet r=p.executeQuery()){
            if(!r.next()||!r.getString(2).startsWith("Prueba S9"))throw new IllegalStateException("Solo se permite una venta sintética S9");
            if(!"REGISTRADA".equals(r.getString(1)))throw new IllegalStateException("La venta debe estar registrada; no repetir la fixture");
          }
        }
        try(PreparedStatement p=c.prepareStatement("select d.producto_id,d.cantidad,p.nombre from detalle_venta d join producto p on p.id=d.producto_id where d.venta_id=?")){
          p.setLong(1,id);try(ResultSet r=p.executeQuery()){
            while(r.next()){
              if(!r.getString(3).startsWith("S9 Tinoco"))throw new IllegalStateException("Producto fuera de la fixture S9");
              try(PreparedStatement u=c.prepareStatement("update producto set stock=stock+? where id=?")){u.setInt(1,r.getInt(2));u.setLong(2,r.getLong(1));u.executeUpdate();}
            }
          }
        }
        try(PreparedStatement p=c.prepareStatement("update ventas set estado='ANULADA' where id=?")){p.setLong(1,id);p.executeUpdate();}
        c.commit();System.out.println("Fixture de venta anulada preparada: "+id);
      }catch(Exception e){c.rollback();throw e;}
    }
  }
}
