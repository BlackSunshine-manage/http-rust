pub trait has_name {
    fn name(&self) -> &str;
    fn new(name: String) -> Self;
}