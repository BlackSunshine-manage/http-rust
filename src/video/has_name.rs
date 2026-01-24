pub trait HasName {
    fn name(&self) -> &str;
    fn new(name: String) -> Self;
}