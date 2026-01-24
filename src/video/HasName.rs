pub trait HasName {
    fn new(name: String) -> Self;
    fn name(&self) -> &str;
}